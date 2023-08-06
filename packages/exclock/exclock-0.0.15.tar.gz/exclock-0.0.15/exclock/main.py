#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
from optparse import OptionParser
from pathlib import Path, PurePath

import json5 as json

from exclock import __VERSION__
from exclock.entities import ClockTimer


def get_title_from_json_filename(json_filename: str) -> str:
    basename = PurePath(json_filename).name
    return basename.split('.')[0].capitalize()


def get_real_json_filename(path: str) -> str:
    path = str(Path(path).expanduser())

    if not Path(path).exists() and Path(path).suffix == '':
        path += ".json5"

    if Path(path).exists():
        return path

    while path.startswith("_"):
        path = path[1:]
    path = str(
        pathlib.Path(__file__).parent.absolute().joinpath("assets").joinpath("clocks").joinpath(
            path))

    return path


def get_option_parser():
    usage = "exclock [filename]"
    parser = OptionParser(usage=usage, version=__VERSION__)

    return parser


def main():
    _, args = get_option_parser().parse_args()
    json_filename = get_real_json_filename(args[0])
    with open(json_filename) as f:
        jdata = json.load(f)
    jdata['title'] = jdata.get('title', get_title_from_json_filename(json_filename))
    clock_timer = ClockTimer.from_dict(jdata)
    clock_timer.run()


if __name__ == '__main__':
    main()
