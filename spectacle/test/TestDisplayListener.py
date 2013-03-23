# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import unittest
from spectacle.main import DisplayListener

class TestCollection(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.myDisplayListener = DisplayListener()

    def tearDown(self):
        """Call after every test case."""
#        self.file.close()

    def testSetCurrent(self):
        """testSetDir. note that all test method names must begin with 'test.'"""
        self.myDisplayListener.setCurrent('/tmp/test.jpg')
