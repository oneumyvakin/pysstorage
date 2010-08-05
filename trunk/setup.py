#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = 'pysstorage',
    version = '0.1',
    packages = find_packages(exclude=['ez_setup', 'tests']),
    author = 'Flier Lu',
    author_email = 'flier.lu@gmail.com',
    description = 'PySStorage is a pure python library to read/write Structured Storage files in COM',
    long_description = open('README.txt').read(),
    license = 'Mozilla Public License 1.1',
    keywords = 'Python COM Storage Filesystem Office',
    url = 'http://code.google.com/p/pysstorage/',
    download_url = 'http://code.google.com/p/pysstorage/downloads/list',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development',
    ]
)