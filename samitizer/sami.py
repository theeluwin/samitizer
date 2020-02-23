# -*- coding: utf-8 -*- #

import os
import re
import codecs
import subprocess

from .const import STAMP_PADDING
from .const import CONVERT_TARGETS
from .subtitle import Subtitle


class Sami:

    def __init__(self, filepath, encoding=None):

        # ready
        self.filepath = filepath
        self.encoding = encoding
        self.raw_text = ''
        self.subtitles = []

        # exploit standard errors
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(f"No such file: '{self.filepath}'")

        # detect encoding
        if self.encoding is None:
            detecting_script = ('/usr/bin/env', 'uchardet', filepath)
            self.encoding = subprocess.check_output(detecting_script).decode('utf-8').strip().lower()

        # read content (if fail, just raise some standard errors)
        with codecs.open(self.filepath, encoding=self.encoding) as fp:
            self.raw_text = fp.read()

        # unify returns
        self.raw_text = self.raw_text.replace('\r\n', '\n')
        self.raw_text = self.raw_text.replace('\n\r', '\n')

        # parse lines
        initial = True
        for line in self.tplit(self.raw_text, 'sync'):

            # parse start stamp
            try:
                stamp = int(self.refind(line, '<sync start=([0-9]+)').group(1))
            except ValueError:
                continue
            except TypeError:
                continue

            # parse content
            lang2content = {}
            raw_paragraphs = self.tplit(line, 'p')
            for raw_paragraph in raw_paragraphs:
                lang = self.refind(raw_paragraph, '<p(.+)class=([a-z]+)').group(2)
                if not lang:
                    continue
                tag_pointer = self.refind(raw_paragraph, '<p(.+)>').end()
                content = raw_paragraph[tag_pointer:]
                content = content.replace('\n', '')
                content = content.replace('&nbsp;', ' ')
                content = content.replace('&nbsp', ' ')
                content = re.sub('<br ?/?>', '\n', content, flags=re.I)
                content = re.sub('<.*?>', '', content)
                content = content.strip()
                if not content:
                    continue
                lang2content[lang] = content
            if not lang2content:
                continue

            # put end stamp to the previous subtitle
            if not initial:
                self.subtitles[-1].end_stamp = stamp
            initial = False

            # gather
            self.subtitles.append(Subtitle(lang2content, stamp))

        # pad end stamp
        self.subtitles[-1].end_stamp = self.subtitles[-1].start_stamp + STAMP_PADDING

    def convert(self, target, lang='ENCC'):

        # ready
        lines = []

        # check supporting formats
        if target not in CONVERT_TARGETS:
            raise NotImplementedError(f"Supporting formats are: {', '.join(CONVERT_TARGETS)}.")

        # vtt format
        if target == 'vtt':
            lines.append('WEBVTT')
            index = 1
            for subtitle in self.subtitles:
                if subtitle.has_lang(lang):
                    line = subtitle.convert(target, lang)
                    line = f"{index}\n{line}"
                    lines.append(line)
                    index += 1
            converted = '\n\n'.join(lines)

        # plain text
        elif target == 'plain':
            for subtitle in self.subtitles:
                if subtitle.has_lang(lang):
                    line = subtitle.convert(target, lang)
                    lines.append(line)
            converted = '\n'.join(lines)

        return converted

    def tplit(self, text, tag):
        delimiter = f'<{tag}'
        tokens = re.split(delimiter, text, flags=re.I)
        if not tokens:
            return []
        dokens = []
        for token in tokens:
            doken = f'{delimiter}{token}'.strip()
            dokens.append(doken)
        return dokens[1:]

    def refind(self, text, pattern):
        return re.search(pattern, text, flags=re.I)
