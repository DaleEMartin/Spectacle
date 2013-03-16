import unittest
import spectacle

class TestCollection(spectacle.Collection):
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
        if self.index() + 1 >= self.num():
            raise StopIteration
        else:
            self.myIndex = self.index() + 1
        return self.get(self.index())

    def prev(self):
        if self.index() - 1 < 0:
            raise StopIteration
        else:
            self.myIndex = self.index() - 1
        return self.get(self.index())

class SlideShowTestCase(unittest.TestCase):

    def setUp(self):
        collection = TestCollection()
        model = spectacle.SlideShowModel(collection)
        self.myModel = model        

    def slideShowModel(self):
        return self.myModel

    def tearDown(self):
        pass

    def testNext(self):
        """testSetDir. note that all test method names must begin with 'test.'"""
        self.assertEqual(self.slideShowModel().next(), "1")
        self.assertEqual(self.slideShowModel().next(), "2")
        self.assertEqual(self.slideShowModel().next(), "3")
        # Asking for the next should raise a StopIteration exception
        self.assertRaises(StopIteration, self.slideShowModel().next)

    def testPrev(self):
        self.slideShowModel().next() # "1"
        self.slideShowModel().next() # "2"
        self.assertEqual(self.slideShowModel().prev(), "1")


        