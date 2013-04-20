# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import unittest
from spectacle.interfaces import DisplayConfig
from spectacle.main import PhotoCache

class MockDisplayConfig(DisplayConfig):
    def __init__(self, cacheDir):
        self.myCacheDir = cacheDir
        
    def cacheDirectory(self):
        return self.myCacheDir

class MockModel(object):
    pass

def makeCache(cacheDir):
    return PhotoCache(MockModel(), MockDisplayConfig(cacheDir))

class TestPhotoCache(unittest.TestCase):
    def setUp(self):
        pass
    
    def photoCache(self):
        return self.myPhotoCache
    
    def testCacheNameAbsolute(self):
        self.myPhotoCache = makeCache("/tmp/mockCacheDir")

        self.assertEquals(self.photoCache().cacheName('this is a test'),
                          '/tmp/mockCacheDir/this_is_a_test')
        
        self.assertEquals(self.photoCache().cacheName('this/is/a/test.jpg'),
                          '/tmp/mockCacheDir/this/is/a/test.jpg')

        self.assertEquals(self.photoCache().cacheName('this/is/a/test.JPG'),
                          '/tmp/mockCacheDir/this/is/a/test.jpg')

        self.assertEquals(self.photoCache().cacheName('this/is/a/test.PnG'),
                          '/tmp/mockCacheDir/this/is/a/test.png')

    def testCacheNameRelative(self):
        self.myPhotoCache = makeCache("mockCacheDir")

        self.assertEquals(self.photoCache().cacheName('this is a test'),
                          'mockCacheDir/this_is_a_test')
        
        self.assertEquals(self.photoCache().cacheName('this/is/a/test.jpg'),
                          'mockCacheDir/this/is/a/test.jpg')

        self.assertEquals(self.photoCache().cacheName('this/is/a/test.JPG'),
                          'mockCacheDir/this/is/a/test.jpg')

        self.assertEquals(self.photoCache().cacheName('this/is/a/test.PnG'),
                          'mockCacheDir/this/is/a/test.png')
