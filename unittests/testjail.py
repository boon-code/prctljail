#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import split, join, normpath, isfile
from tempfile import mkdtemp
from shutil import rmtree
import sys
import unittest

magic_number = 5
magic_text = "It's pure magic."


def _good_simple():
    return magic_number


def _good_io(f):
    f.write(magic_text)
    f.flush()
    return (magic_number, 3)


def _bad_io(badfile):
    with open(badfile, 'w') as f:
        f.write(magic_text)
    return magic_number


def _do_import():
    import base64


class TestJailedProcess(unittest.TestCase):
    
    def setUp(self):
        self.path = mkdtemp(prefix='prctljail_')
        self.good_path = join(self.path, "good.txt")
        self.bad_path = join(self.path, "bad.txt")
    
    def test_valid_simple(self):
        a = JailedProcess(_good_simple)
        ret = a.run()
        self.assertEqual(ret, 0)
    
    def test_valid_io(self):
        with open(self.good_path, 'w') as f:
            a = JailedProcess(_good_io, args=[f])
            ret = a.run()
            self.assertEqual(ret, 0)
        self.assertTrue(isfile(self.good_path))
        
        with open(self.good_path, 'r') as f:
            data = f.read()
        
        self.assertEqual(data, magic_text)
    
    def test_invalid_import(self):
        a = JailedProcess(_do_import)
        ret = a.run()
        self.assertEqual(ret, 9)
        
    def test_invalid_io(self):
        a = JailedProcess(_bad_io, args=[self.bad_path])
        ret = a.run()
        self.assertEqual(ret, 9)
    
    def tearDown(self):
        rmtree(self.path)


if __name__ == '__main__':
    base = split(sys.argv[0])[0]
    path = normpath(join(base, "../src/"))
    sys.path.insert(0, path)
    from prctljail import JailedProcess
    if JailedProcess.isAvailable():
        unittest.main()
    else:
        sys.stderr.write("Sorry, this feature isn't available on your\
 platform")
