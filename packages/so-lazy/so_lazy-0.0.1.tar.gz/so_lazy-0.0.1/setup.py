#!/usr/bin/env python

'''Setup configuration for so_lazy package'''

import json
import setuptools

PKG_NAME = 'so_lazy'

with open(PKG_NAME + '/pkg_info.json') as fh:
    _pkg_info = json.load(fh)

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name=PKG_NAME,
    version=_pkg_info['version'],
    author=_pkg_info['author'],
    description=_pkg_info['description'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=_pkg_info['homepage'],
    download_url=_pkg_info['download'],
    license=_pkg_info['license'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.5'
)
