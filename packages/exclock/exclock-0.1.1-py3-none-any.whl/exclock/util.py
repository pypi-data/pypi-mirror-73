#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
from glob import glob
from pathlib import Path


class DummyNotifier:

    @classmethod
    def notify(message):
        ...


def is_time_str(s: str) -> bool:
    if s == "":
        return False

    if s.isdigit():
        return True

    mind = s.find("m")
    if mind != -1:
        s = s[mind + 1:]

    sind = s.find("s")
    if sind != -1:
        s = s[sind + 1:]

    return s == ""


def get_real_json_filename(path: str) -> str:
    path = str(Path(path).expanduser())
    basedir = Path("~/.exclock/clock/").expanduser()

    if not Path(path).exists() and not Path(str(basedir) + "/" +
                                            path).exists() and Path(path).suffix == '':
        path += ".json5"

    if Path(path).exists():
        return path

    if basedir.exists():
        res = glob(str(basedir) + "/" + path)
        if res:
            return res[0]

    while path.startswith("_"):
        path = path[1:]
    path = str(
        pathlib.Path(__file__).parent.absolute().joinpath("assets").joinpath("clock").joinpath(
            path))

    return path


def get_real_sound_filename(path: str) -> str:
    path = str(Path(path).expanduser())

    if Path(path).exists():
        return path

    basedir = Path("~/.exclock/sound/").expanduser()
    if basedir.exists():
        res = glob(str(basedir) + "/" + path)
        if res:
            return res[0]

    while path.startswith("_"):
        path = path[1:]

    return str(
        pathlib.Path(__file__).parent.absolute().joinpath("assets").joinpath("sound").joinpath(
            path))
