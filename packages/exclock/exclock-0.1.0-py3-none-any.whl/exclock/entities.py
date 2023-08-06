#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import pathlib
from dataclasses import dataclass
from pathlib import Path
from time import sleep as time_sleep
from typing import Callable, Dict, List, Optional

import vlc

try:
    from pync import Notifier
except Exception:
    from util import DummyNotifier as Notifier

DEFAULT_TITLE = "ExClock"


def get_time_from_str(s: str) -> int:
    if s.isdigit():
        return int(s)
    else:
        res = 0
        m_ind = s.find("m")
        if m_ind != -1:
            res += 60 * int(s[:m_ind])

        s_ind = s.find("s")
        if s_ind == -1:
            return res
        res += int(s[m_ind + 1:s_ind])
        return res


def inner_str(s: str, d: dict) -> str:
    starts: List[int] = []
    ends: List[int] = []
    for i, c in enumerate(s):
        if len(starts) == len(ends) and c == "{":
            starts.append(i)
        if len(starts) == len(ends) + 1 and c == "}":
            ends.append(i)

    calcs = dict()
    for start, end in zip(starts, ends):
        target = s[start + 1:end]
        calcs[target] = eval(target, {}, d)

    for key, val in calcs.items():
        s = s.replace("{" + key + "}", str(val))
    return s


def confirm_dummy():
    ...


def confirm_input():
    input(">>> ")


def conv_confirm_f(s: str) -> Callable:
    s = s.lower()
    if s == 'input':
        return confirm_input
    else:
        return confirm_dummy


def get_real_filename(path: str) -> str:
    path = str(Path(path).expanduser())

    if Path(path).exists():
        return path

    while path.startswith("_"):
        path = path[1:]

    return str(
        pathlib.Path(__file__).parent.absolute().joinpath("assets").joinpath("musics").joinpath(
            path))


@dataclass
class Sound:
    message: str
    sound_filename: str
    confirm_f: Callable

    def __post_init__(self):
        self.sound_filename = get_real_filename(self.sound_filename)

    def run(self):
        p = vlc.MediaPlayer(self.sound_filename)
        p.play()
        return p

    @classmethod
    def from_dict(cls, json: dict) -> Sound:
        return Sound(
            message=json["message"],
            sound_filename=json["sound_filename"],
            # confirm_f=conv_confirm_f(json["confirm"])
            confirm_f=confirm_dummy)

    def __eq__(self, other) -> bool:
        return self.message == other.message and self.sound_filename == other.sound_filename


def any_ended_sounds(ps):
    for p in ps:
        if p.get_state() != vlc.State.Ended:
            return False

    return True


@dataclass
class ClockTimer:
    message: str
    sounds: Dict[int, Sound]  # Dict from sec to sound
    loop: Optional[int]
    title: str

    @property
    def sorted_sounds(self) -> Dict[int, Sound]:
        return {sec: self.sounds[sec] for sec in sorted(self.sounds)}

    def run_once(self, count):
        sounds = self.sorted_sounds

        t = 0
        ps = []

        while True:
            for sec, sound in sounds.items():
                if t == sec:
                    message = inner_str(sound.message, {"count": count})
                    Notifier.notify(message, title=self.title)
                    sound.confirm_f()
                    ps.append(sound.run())

            if len(sounds) == len(ps) and any_ended_sounds(ps):
                break

            t += 1
            time_sleep(1)

        while not any_ended_sounds(ps):
            time_sleep(1)

    def run(self):
        count = 1
        if type(self.loop) == int:
            for _ in range(self.loop):
                self.run_once(count=count)
                count += 1
        else:
            while True:
                self.run_once(count=count)
                count += 1

    @classmethod
    def from_dict(cls, json):
        sounds = {}
        for sec, sound in json["sounds"].items():
            sec = get_time_from_str(sec)
            sounds[sec] = Sound.from_dict(sound)

        return ClockTimer(
            message=json["message"], sounds=sounds, loop=json["loop"], title=json["title"])


if __name__ == '__main__':
    confirm_f = confirm_dummy  # noqa: E231
    sound = Sound(message="message", sound_filename="music.mp3", confirm_f=confirm_f)
    sound2 = Sound(message="message", sound_filename="music2.mp3", confirm_f=confirm_f)
    clock_timer = ClockTimer("message", sounds={0: sound, 2: sound2}, loop=2, title="abc.json5")
    clock_timer.run()
