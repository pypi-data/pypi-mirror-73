#!/usr/bin/env python
# -*- coding: utf-8 -*-
from io import open
from setuptools import setup

"""
:authors: Warale
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2020 Warale
"""


version = '1.0'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='new_vk',
    version=version,

    author='Warale',
    author_email='waralegit@yandex.ru',

    description=(
        u'Python модуль для написания скриптов для социальной сети '
        u'Вконтакте (vk.com) (API wrapper)'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/Warale/new_vk',
    download_url='https://github.com/Warale/new_vk/archive/master.zip',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['new_vk', 'jconfig'],
    install_requires=['requests', 'enum34;python_version<"3.4"', 'six'],
    extras_require={
        'vkstreaming': ['websocket-client'],
        'vkaudio': ['beautifulsoup4'],
    },

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
