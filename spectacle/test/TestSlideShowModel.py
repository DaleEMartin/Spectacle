# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import unittest
from spectacle.interfaces import Collection
from spectacle.interfaces import CollectionConfig
from spectacle.interfaces import DisplayConfig
from spectacle.interfaces import SlideShowListener
from spectacle.main import SlideShowModel
from spectacle.main import Spectacle

class MockCollectionConfig(CollectionConfig):
    pass

class MockDisplayConfig(DisplayConfig):
    pass

class MockCollection(Collection):
    def __init__(self):
        self.myPics = list()
        self.pics().append("1")
        self.pics().append("2")
        self.pics().append("3")
        self.myIndex = -1

    def index(self):
        return self.myIndex

    def num(self):
        return len(self.pics())

    def pics(self):
        return self.myPics

    def get(self, index):
        return self.pics()[index]

    def next(self):
        if self.peekNext() < self.index():
            raise StopIteration
        else:
            self.myIndex = self.peekNext();
        return self.get(self.index())

    def prev(self):
        if self.index() - 1 < 0:
            raise StopIteration
        else:
            self.myIndex = self.index() - 1
        return self.get(self.index())

    def peekNext(self):
        if self.index() + 1 >= self.num():
            return 0
        else:
            return self.index() + 1

    def collection(self):
        return self

class MockListener(SlideShowListener):
    def __init__(self):
        self.myCurrent = ""
        self.myQuitCalled = False;
        
    def current(self):
        return self.myCurrent;
    
    def setCurrent(self, newCurrent):
        self.myCurrent = newCurrent;

    def setNext(self, newNext):
        pass
        
    def quit(self):
        self.myQuitCalled = True;

    def quitCalled(self):
        return self.myQuitCalled;

class SlideShowTestCase(unittest.TestCase):

    def setUp(self):
        spectacle = Spectacle(True, MockCollectionConfig(), MockDisplayConfig())
        collection = MockCollection()
        model = SlideShowModel(collection)
        self.myListener = MockListener()
        model.addListener(self.myListener)
        self.myModel = model        

    def listener(self):
        return self.myListener;

    def slideShowModel(self):
        return self.myModel

    def tearDown(self):
        pass

    def testNext(self):
        """testSetDir. note that all test method names must begin with 'test.'"""
        self.assertEqual(self.slideShowModel().next(), "1")
        self.assertEqual(self.listener().current(), "1")
        self.assertEqual(self.slideShowModel().next(), "2")
        self.assertEqual(self.listener().current(), "2")
        self.assertEqual(self.slideShowModel().next(), "3")
        self.assertEqual(self.listener().current(), "3")
        # Asking for the next should raise a StopIteration exception
        self.assertRaises(StopIteration, self.slideShowModel().next)

    def testPrev(self):
        self.slideShowModel().next() # "1"
        self.slideShowModel().next() # "2"
        self.assertEqual(self.slideShowModel().prev(), "1")
        self.assertEqual(self.listener().current(), "1")
        
    def testQuit(self):
        systemExitCalled = False
        try:
            self.slideShowModel().quit();            
        except SystemExit:
            systemExitCalled = True
        self.assertEqual(self.listener().quitCalled(), True)
        self.assertEqual(systemExitCalled, True)
        