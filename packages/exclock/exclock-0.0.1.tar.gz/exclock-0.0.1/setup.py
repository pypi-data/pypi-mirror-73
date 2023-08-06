#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="exclock",
    version="0.0.1",
    entry_points={"console_scripts": ["exclock=exclock.main:main"]},
)
