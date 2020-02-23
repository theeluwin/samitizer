# -*- coding: utf-8 -*-

from .const import STAMP_PADDING
from .const import CONVERT_TARGETS


class Subtitle:

    def __init__(self, lang2content, start_stamp, end_stamp=STAMP_PADDING):
        self.lang2content = lang2content
        self.start_stamp = start_stamp
        self.end_stamp = end_stamp

    def has_lang(self, lang):
        return lang in self.lang2content

    def convert(self, target, lang):

        # check supporting formats
        if target not in CONVERT_TARGETS:
            raise NotImplementedError(f"Supporting formats are: {', '.join(CONVERT_TARGETS)}.")

        # if lang is not supported, return blank
        content = self.lang2content.get(lang, '')

        # vtt format
        if target == 'vtt':
            start_vtt = self.stamp2vtttime(self.start_stamp)
            end_vtt = self.stamp2vtttime(self.end_stamp)
            return f"{start_vtt} --> {end_vtt}\n{content}"

        # plain text
        elif target == 'plain':
            return content

    def stamp2vtttime(self, stamp):
        ms = stamp % 1000
        s = int(stamp / 1000)
        m = int(s / 60) % 60
        h = int(s / 3600)
        s = s % 60
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

    def __str__(self):
        if not self.lang2content:
            return ''
        lang = list(self.lang2content.keys())[0]
        representative = self.lang2content[lang]
        return f"[{self.start_stamp}:{self.end_stamp}] {representative}"
