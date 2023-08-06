#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from exclock import __VERSION__

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Multimedia :: Sound/Audio :: Players :: MP3",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Version Control :: Git",
    "Topic :: Software Development",
    "Topic :: Terminals",
    "Topic :: Utilities",
]

setup(
    name="exclock",
    version=__VERSION__,
    description="exclock is a cui extended timer.",
    long_description=open("Readme.rst").read(),
    author="yassu",
    author_email='yasu0320.dev@gmail.com',
    entry_points={"console_scripts": ["exclock=exclock.main:main"]},
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=[
        "python-vlc",
        "json5",
        "notify-py",
    ],
    include_package_data=True,
    url='https://gitlab.com/yassu/exclock',
)
