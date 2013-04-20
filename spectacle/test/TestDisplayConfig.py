# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import unittest
import time
from spectacle.main import PygameDisplayConfig


class TestDisplayConfig(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        pass

    def tearDown(self):
        """Call after every test case."""
        pass

    def testReadConfig1(self):
        """testSetDir. note that all test method names must begin with 'test.'"""
        self.assertEquals(False, True)
