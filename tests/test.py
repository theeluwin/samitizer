# -*- coding: utf-8 -*-

import os
import unittest

from samitizer import Smi


class TestSamitizer(unittest.TestCase):

    def setUp(self):
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        self.smi_filepath = os.path.join(data_dir, 'sample.smi')
        with open(os.path.join(data_dir, 'sample.vtt')) as fp:
            self.vtt_text = fp.read()
        with open(os.path.join(data_dir, 'sample.txt')) as fp:
            self.plain_text = fp.read()

    def test_parsed(self):
        smi = Smi(self.smi_filepath)
        self.assertEqual(len(smi.subtitles), 3)

    def test_convert_vtt(self):
        smi = Smi(self.smi_filepath)
        vtt_text = smi.convert('vtt', 'KRCC')
        self.assertEqual(vtt_text, self.vtt_text)

    def test_convert_plain(self):
        smi = Smi(self.smi_filepath)
        plain_text = smi.convert('plain', 'KRCC')
        self.assertEqual(plain_text, self.plain_text)


if __name__ == '__main__':
    unittest.main()
