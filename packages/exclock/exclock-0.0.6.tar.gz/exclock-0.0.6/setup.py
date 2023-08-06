#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from exclock import __VERSION__

classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: MacOS X",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: MacOS",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
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
    description="exclock is a cui extended timer for mac OS.",
    long_description=open("Readme.rst").read(),
    author="yassu",
    author_email='yasu0320.dev@gmail.com',
    entry_points={"console_scripts": ["exclock=exclock.main:main"]},
    classifiers=classifiers,
    packages=find_packages(),
    package_data={
        "assets": ["*.mp3"],
        "examples": ["*.json5"],
    },
    install_requires=[
        "python-vlc",
        "json5",
        "pync",
    ],
    url='https://gitlab.com/yassu/exclock',
)
