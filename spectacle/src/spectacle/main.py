# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved.
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

from spectacle.interfaces import *

class Spectacle(object):
#    def __init__(self, initial_balance=0):
#        self.balance = initial_balance
    def __init__(self):
        self.dir = ""
        
    def directory(self):
        return self.dir  

    def setDirectory(self, newDirectory):
        self.dir = newDirectory
        
class SlideShowModel(object):
    def __init__(self, aCollection):
        self.myCollection = aCollection
        self.listeners = list()
        self.myCurrent = ""
    
    def collection(self):
        return self.myCollection
    
    def addListener(self, aListener):
        self.listeners.append(aListener)
    
    def next(self):
        self.myCurrent = self.collection().iter().next()
        for listener in self.listeners:
            listener.setCurrent(self.myCurrent)
        return self.myCurrent
    
    def prev(self):
        self.myCurrent = self.collection().iter().prev()
        for listener in self.listeners:
            listener.setCurrent(self.myCurrent)
        return self.myCurrent
    
    def current(self):
        return self.myCurrent

class DisplayListener(SlideShowListener):
    """This abstract class is responsible for defining the interface of a SlideShowListener."""
    def __init__(self):
        pass
    
    def current(self):
        pass
    
    def setCurrent(self, newCurrent):
        pass
