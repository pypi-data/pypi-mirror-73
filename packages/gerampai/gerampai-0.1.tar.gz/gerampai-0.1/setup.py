import re

from setuptools import setup, find_packages
from os import path


BASE_DIR = path.abspath(path.dirname(__file__))

with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_version():
    with open('src/gerampai.py', 'r') as f:
        content = f.read()

    version = re.findall(r"version[\s+='_\"]+(.*)['\"]", content)

    return version[0]

setup(
    name='gerampai',
    version=get_version(),
    description='Instagram extractor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/wakataw/gerampai',
    author='Agung Pratama',
    author_email='agungpratama1001@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Natural Language :: English',
        'Natural Language :: Indonesian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.5',
    install_requires=[
        'instagram-private-api'
    ],
    entry_points={
        'console_scripts': ['gerampai=src.gerampai:main']
    },
    project_urls={
        'Bug Reports': 'https://gitlab.com/wakataw/gerampai/issues',
        'Source': 'https://gitlab.com/wakataw/gerampai'
    },
    keywords='instagram, scraper, data, extractor',
    packages=find_packages(exclude=['tests', 'examples']),
    zip_safe=True,
    license='MIT'
)