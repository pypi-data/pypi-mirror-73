import csv
import hashlib
import os
import string
import random
import argparse
import tempfile
import shutil
import re
from datetime import datetime
from time import sleep
from instagram_web_api import Client


def print_header():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, '__init__.py'), 'r') as f:
        content = f.read()

    version = re.findall(r"version[\s+='_\"]+(.*)['\"]", content)

    print("""   ______                                      _ 
  / ____/__  _________ _____ ___  ____  ____ _(_)
 / / __/ _ \/ ___/ __ `/ __ `__ \/ __ \/ __ `/ / 
/ /_/ /  __/ /  / /_/ / / / / / / /_/ / /_/ / /  
\____/\___/_/   \__,_/_/ /_/ /_/ .___/\__,_/_/   
          Instagram Extractor /_/ Ver. {}
""".format(version[0]))


class MaxRetryException(Exception):
    pass


class CustomClient(Client):

    max_retry = 3
    delay_time = 1

    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode()).hexdigest()

    def extract_feed(self, user_id, retry=0, **kwargs):
        try:
            feed = self.user_feed(user_id, **kwargs)
        except Exception as e:
            print(e)
            sleep(60)
            retry += 1

            if retry > self.max_retry:
                raise MaxRetryException("Max retry exceeded")
            else:
                if retry == 1:
                    print()
                print("Retry {}".format(retry))
                feed = self.extract_feed(user_id, retry=retry, **kwargs)

        return feed


def convert_unixtime(data):
    try:
        return datetime.utcfromtimestamp(int(data)).strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return ''


def write(results, username):
    filename = None

    with tempfile.NamedTemporaryFile(mode='w+t', delete=False, encoding='utf-8', newline='') as temp_results:
        filename = temp_results.name
        writer = csv.writer(temp_results, quotechar='"', quoting=csv.QUOTE_ALL)

        writer.writerow(['id', 'is_video', 'comment_disabled', 'taken_at_timestamp', 'taken_at', 'owner_id',
                         'owner_username', 'viewer_has_liked', 'viewer_has_saved', 'viewer_has_saved_to_collection',
                         'viewer_in_photo_of_you', 'thumbnail_src', 'link', 'caption_text', 'user_has_liked',
                         'user_id', 'user_username', 'type', 'likes_count', 'comments_count', 'location',
                         'created_timestamp', 'created_time'])

        for item in results:
            node = item['node']
            row = [
                node['id'],
                node['is_video'],
                node['comments_disabled'],
                node['taken_at_timestamp'],
                convert_unixtime(node['taken_at_timestamp']),
                node['owner']['id'],
                node['owner']['username'],
                node['viewer_has_liked'],
                node['viewer_has_saved'],
                node['viewer_has_saved_to_collection'],
                node['viewer_in_photo_of_you'],
                node['thumbnail_src'],
                node['link'],
                ' '.join(node['caption']['text'].split()) if node['caption'] is not None else '',
                node['user_has_liked'],
                node['user']['id'],
                node['user']['username'],
                node['type'],
                node['likes']['count'],
                node['comments']['count'],
                node['location'],
                node['created_time'],
                convert_unixtime(node['created_time']),
            ]

            writer.writerow(row)

    shutil.copy(filename, '{}.csv'.format(username))
    os.remove(filename)

    print("Save results to {0}.csv and {0}-profile.txt".format(username))


def print_profile(profile):
    simplify_profile = """User Profile
Username           : @{}
Full Name          : {}
Bussines Account   : {}
Bussiness Category : {}
Private            : {}
Verified           : {}
Website            : {}
Total Post         : {}
Followers          : {}
Following          : {}
Biography          : {}
    """.format(
        profile['username'], profile['full_name'], profile['is_business_account'], profile['business_category_name'],
        profile['is_private'], profile['is_verified'], profile['website'], profile['counts']['media'],
        profile['counts']['followed_by'],
        profile['counts']['follows'], ' '.join(profile['biography'].split())
    )
    with open(profile['username']+'-profile.txt', 'w', encoding='utf-8') as f:
        f.write(simplify_profile)

    print(simplify_profile)

def extract_client(client, args):
    user = client.user_info2(args.username)
    print_profile(user)

    total_media = user['counts']['media']
    total = 0
    user_id = user['id']
    user_feed = client.extract_feed(user_id, count=args.page_size, extract=False)
    user_data = user_feed['data']['user']['edge_owner_to_timeline_media']

    if user_data['edges']:
        total += len(user_data['edges'])
        for node in user_data['edges']:
            yield node

    has_next = user_data['page_info']['has_next_page']
    next_max_id = user_data['page_info']['end_cursor']

    while has_next:
        sleep(args.delay)
        user_feed = client.extract_feed(user_id, count=args.page_size, extract=False, max_id=next_max_id)
        user_data = user_feed['data']['user']['edge_owner_to_timeline_media']
        if user_data['edges']:
            total += len(user_data['edges'])
            for node in user_data['edges']:
                yield node
        has_next = user_data['page_info']['has_next_page']
        next_max_id = user_data['page_info']['end_cursor']

        print('Extracting {} of {} data ({:,.2f}%)'.format(total, total_media, total/total_media*100), end='\r')

    print()


def main():
    print_header()
    parser = argparse.ArgumentParser(description='Instagram extractor.')
    parser.add_argument('username', type=str, help='Username instagram.')
    parser.add_argument('--delay', type=int, default=1, help="Delay untuk setiap iterasi halaman.")
    parser.add_argument('--page-size', type=int, default=12, help="Jumlah post per halaman. Maksimal 50 posts.")
    parser.add_argument('--max-retry', type=int, default=3, help="Maximum retry jika terjadi kegagalan pada saat iterasi halaman feed.")

    args = parser.parse_args()

    client = CustomClient(auto_patch=True, drop_incompat_keys=False, timeout=300)
    client.max_retry = args.max_retry
    client.delay_time = args.delay

    results = extract_client(client, args)
    write(results, args.username)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Canceled by user, bye!")