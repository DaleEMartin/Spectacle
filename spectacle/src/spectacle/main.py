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
# import time

from spectacle.interfaces import SlideShowListener
from spectacle.interfaces import Collection

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

        nextPic = self.pictureList[self.myIdx]
        if self.verbose():
            print "nextPic: " + nextPic

        return nextPic

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
        self.mySlideshowModel.next()
        pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
        i = 0;
        while True:
            event = pygame.event.wait()
            if (event.type == pygame.USEREVENT + 1):
                print "pygame.USEREVENT"
                self.mySlideshowModel.next()
                # If we took so long another USEREVENT posted
                # we're going to clear it so that quit events
                # can make it through
                pygame.event.clear(pygame.USEREVENT + 1)
            elif (event.type == pygame.QUIT):
                print "pygame.QUIT"
                pygame.quit()
                sys.exit()
            elif (event.type == pygame.KEYDOWN):
                print "pygame.KEYDOWN"
                pygame.quit()
                sys.exit()
            elif (i == 10):
                print "i == 10"
                pygame.quit()
                sys.exit()

            # i = i + 1
            # pygame.time.wait(100)
        
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
    def __init__(self, verbose):
        self.initDisplay()
        self.myCurrent = ""
        self.myVerbose = verbose
        
    def verbose(self):
        return self.myVerbose;
        
    def initDisplay(self):
        pygame.init()
        displayInfo = pygame.display.Info();
        self.screenWidth = displayInfo.current_w;
        self.screenHeight = displayInfo.current_h;
        self.myDisplay = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.FULLSCREEN)
        pygame.mouse.set_visible(0)        
        
    def current(self):
        return self.myCurrent
    
    def setCurrent(self, newCurrent):
        self.myCurrent = newCurrent
        self.display(newCurrent)

    def prepareImage(self, image):
        pilImage = Image.open(image)
        pilConverted = pilImage.convert('RGB')

        width, height = pilConverted.size
        ratio = min(self.screenWidth/float(width), self.screenHeight/float(height))
        
        newWidth = int(ratio * width)
        newHeight = int(ratio * height)

        if (self.verbose()):
            print "ratio: " + str(ratio)
            print "newWidth: " + str(newWidth)
            print "newHeight: " + str(newHeight)

        return pilConverted.resize([newWidth, newHeight], Image.ANTIALIAS)
        

    def display(self,image):
        image = self.prepareImage(image)

        pilString = image.tostring()
        pygameImage = pygame.image.fromstring(pilString,
                                              image.size,
                                              'RGB')
        self.myDisplay.fill((0, 0, 0))

        scaledWidth, scaledHeight = image.size

        extraHeight = self.screenHeight - scaledHeight;
        extraWidth  = self.screenWidth - scaledWidth;

        self.myDisplay.blit(pygameImage, (extraWidth/2, extraHeight/2))

        pygame.display.update()
