#!/usr/bin/env python

from setuptools import setup

setup(
    name='aioymaps',
    version='1.0.0',
    description='Async client for Yandex Maps',
    author='Ivan Belokobylskiy',
    author_email='belokobylskij@gmail.com',
    url='https://github.com/devbis/aioymaps/',
    py_modules=['aioymaps'],
    install_requires=['aiohttp>=3.0.0'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
)
