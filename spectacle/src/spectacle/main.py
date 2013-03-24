# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved.
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import Image
import os
import pygame
import sqlite3 as lite
import sys
import time

from spectacle.interfaces import SlideShowListener
from spectacle.interfaces import Collection

screenWidth = 1024
screenHeight = 768

class PictureDB(object):
    def __init__(self, dbDir, verbose):
        self.myDBDir = dbDir
        self.myVerbose = verbose
            
    def initDB(self):
        con = lite.connect('test.db')
        cur = con.cursor()    
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()
    
        print "SQLite version: %s" % data
        

class DefaultCollection(Collection):
    def __init__(self, config, verbose):
        self.myConfig = config
        self.myVerbose = verbose
        self.myPictureDirectories = config.get('Collection', 'PictureDirectories')
        if (self.myVerbose):
            print "self.myPictureDirectories: " + self.myPictureDirectories         
        self.myDBDirectory = config.get('Collection', 'DBDirectory')
        if (self.myVerbose):
            print "self.myDBDirectory: " + self.myDBDirectory         
        self.pictureList = []
        self.myIdx = -1
    
    def verbose(self):
        return self.myVerbose
    
    def addPic(self, picture):
        if (self.verbose()):
            print "adding: " + picture
        self.pictureList.append(picture)
    
    def pictureDirectories(self):
        if type(self.myPictureDirectories) is list:
            return self.myPictureDirectories
        else:
            return [self.myPictureDirectories]

    def scanPictures(self, pictureDirectories):
        for currentDir in pictureDirectories:
            dirListing = os.listdir(currentDir)
            for entry in dirListing:
                if os.path.isdir(entry):
                    if (self.verbose()):
                        print "dir: " + entry
                    self.scanPictures(entry)
                elif entry.endswith('.jpg'):
                    self.addPic(currentDir + "/" + entry)
                else:
                    if (self.verbose()):
                        print "nothing: " + entry

    def initDB(self):
        self.scanPictures(self.pictureDirectories())
        
    def next(self):
        if (self.myIdx + 1 < len(self.pictureList)):
            self.myIdx = self.myIdx + 1
        else:
            self.myIdx = 0

        next = self.pictureList[self.myIdx]
        if self.verbose():
            print "next: " + next

        return next

class Spectacle(object):
    def __init__(self, verbose, config):
        self.dir = ""
        self.myConfig = config
        self.myVerbose = verbose
        
    def config(self):
        return self.myConfig
    
    def verbose(self):
        return self.myVerbose
        
    def doit(self):
        self.myCollection = DefaultCollection(self.config(), self.verbose())
        self.myCollection.initDB();
        self.mySlideshowModel = SlideShowModel(self.myCollection)
        self.mySlideshowModel.addListener(DisplayListener())
        # self.myCollection = SimpleCollection(collectionConfig()) 
        pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
        i = 0;
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    print "pygame.QUIT"
                    sys.exit()
                elif (event.type == pygame.KEYDOWN):
                    print "pygame.KEYDOWN"
                    sys.exit()
                elif (i == 4):
                    print "i == 4"
                    sys.exit()

                self.mySlideshowModel.next()
                i = i + 1
                pygame.time.wait(100)
        
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
        self.myDisplay = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
        self.myCurrent = ""
        
    def current(self):
        return self.myCurrent
    
    def setCurrent(self, newCurrent):
        self.myCurrent = newCurrent
        self.display(newCurrent)
        
    def display(self,image):
        pilImage = Image.open(image)
        pilConverted = pilImage.convert('RGB')

        width, height = pilConverted.size
        ratio = min(screenWidth/float(width), screenHeight/float(height))
        newWidth = int(ratio * width)
        newHeight = int(ratio * height)
        pilConverted.thumbnail([newWidth, newHeight], Image.ANTIALIAS)

        pilString = pilConverted.tostring()
        pygameImage = pygame.image.fromstring(pilString,
                                              pilConverted.size,
                                              'RGB')
        pygameImage = pygame.transform.scale(pygameImage,(width,height))
        self.myDisplay.blit(pygameImage, (0, 0))
        pygame.display.update()
