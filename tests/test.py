# -*- coding: utf-8 -*-

import os
import unittest

from os.path import join as pjoin
from samitizer import Sami


class TestSamitizer(unittest.TestCase):

    def setUp(self):
        data_dir = pjoin(os.path.dirname(os.path.abspath(__file__)), 'data')
        self.sami_filepath = pjoin(data_dir, 'sample.smi')
        with open(pjoin(data_dir, 'sample.vtt')) as fp:
            self.vtt_text = fp.read().strip()
        with open(pjoin(data_dir, 'sample.txt')) as fp:
            self.plain_text = fp.read().strip()
        with open(pjoin(data_dir, 'str_test.txt')) as fp:
            self.str_subtitles = fp.read().strip().split('\n')

    def test_filepath_fail(self):
        with self.assertRaises(FileNotFoundError):
            Sami('fail')

    def test_parsed(self):
        sami = Sami(self.sami_filepath)
        self.assertEqual(len(sami.subtitles), 3)

    def test_convert_vtt(self):
        sami = Sami(self.sami_filepath)
        vtt_text = sami.convert('vtt', 'KRCC')
        self.assertEqual(vtt_text, self.vtt_text)

    def test_convert_plain(self):
        sami = Sami(self.sami_filepath)
        plain_text = sami.convert('plain', 'KRCC')
        self.assertEqual(plain_text, self.plain_text)

    def test_convert_target_fail(self):
        sami = Sami(self.sami_filepath)
        with self.assertRaises(NotImplementedError):
            sami.convert('fail', 'KRCC')

    def test_str(self):
        sami = Sami(self.sami_filepath)
        for subtitle, str_subtitle in zip(sami.subtitles, self.str_subtitles):
            self.assertEqual(str(subtitle), str_subtitle)


if __name__ == '__main__':
    unittest.main()
