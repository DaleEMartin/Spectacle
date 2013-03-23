# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import unittest
from spectacle.main import Spectacle

class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.spectacle = Spectacle()
#        self.foo = Foo()
#        self.file = open( "blah", "r" )

    def tearDown(self):
        """Call after every test case."""
#        self.file.close()

    def testSetDir(self):
        """testSetDir. note that all test method names must begin with 'test.'"""
        self.spectacle.setDirectory("foo")
        assert self.spectacle.directory() == "foo", "Directory didn't get set correctly"
#        assert foo.bar() == 543, "bar() not calculating values correctly"

#    def testB(self):
#        """test case B"""
#        assert foo+foo == 34, "can't add Foo instances"
#
#    def testC(self):
#        """test case C"""
#        assert foo.baz() == "blah", "baz() not returning blah correctly"
