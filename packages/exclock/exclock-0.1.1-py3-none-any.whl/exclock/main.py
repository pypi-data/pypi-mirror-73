#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from pathlib import Path, PurePath
from sys import stderr

import json5 as json

from exclock import __VERSION__
from exclock.entities import ClockTimer
from exclock.util import get_real_json_filename, get_real_sound_filename, is_time_str


def get_title_from_json_filename(json_filename: str) -> str:
    basename = PurePath(json_filename).name
    return basename.split('.')[0].capitalize()


def check_raw_clock(d) -> None:
    if type(d) != dict:
        raise ValueError("clock file err: doesn't mean dict.")

    if "message" not in d:
        raise ValueError("clock file err: doesn't include message property.")

    if type(d["message"]) != str:
        raise ValueError(f"clock file err: {d['message']} is not str object.")

    if "sounds" not in d:
        raise ValueError("clock file err: doesn't include sounds property.")

    if type(d["sounds"]) != dict:
        raise ValueError("clock file err: sounds is not dict object.")

    # sound["n"]はdict
    # soundsのmessageがある
    # soundsのmessageは文字列型
    # sounds_filenameがある
    # sounds_filenameの値は文字列
    # loopがなかったらエラー
    # loopの値は0以上の整数
    # titleがあるならば その値は文字列

    for time_s, sound in d["sounds"].items():
        if not is_time_str(time_s):
            raise ValueError(f"clock file err: {time_s} is not time.")

        filename = get_real_sound_filename(sound["sound_filename"])
        if not Path(filename).exists():
            raise FileNotFoundError(f"clock file err: {sound['sound_filename']} is not found.")


def get_option_parser():
    usage = "exclock [filename]"
    parser = OptionParser(usage=usage, version=__VERSION__)

    return parser


def main():
    _, args = get_option_parser().parse_args()

    if len(args) != 1:
        print("Length of argument should be 1.", file=sys.stderr)
        sys.exit(1)

    json_filename = get_real_json_filename(args[0])
    try:
        with open(json_filename) as f:
            jdata = json.load(f)
    except ValueError as err:
        print(
            f"{json_filename} is Incorrect format for json5:\n" + f"    {err.args[0]}",
            file=stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"{args[0]} is not found.", file=sys.stderr)
        sys.exit(1)

    try:
        check_raw_clock(jdata)
    except Exception as err:
        print(err.args[0], file=stderr)
        sys.exit(1)

    jdata['title'] = jdata.get('title', get_title_from_json_filename(json_filename))
    clock_timer = ClockTimer.from_dict(jdata)
    clock_timer.run()


if __name__ == '__main__':
    main()
