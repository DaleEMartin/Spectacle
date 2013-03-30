# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved.
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import Image
import os
import pygame
import sys
# import time

from spectacle.interfaces import SlideShowListener
from spectacle.interfaces import Collection
from spectacle.interfaces import CollectionConfig

# A wrapper around the ConfigParser object
class DefaultCollectionConfig(CollectionConfig):
    def __init__(self, configParser, verbose):
        self.myVerbose = verbose
        self.myPictureDirectories = configParser.get('Collection', 'PictureDirectories')
        self.myDBDirectory = configParser.get('Collection', 'DBDirectory')

        if (self.myVerbose):
            print "self.myPictureDirectories: " + self.myPictureDirectories         
        if (self.myVerbose):
            print "self.myDBDirectory: " + self.myDBDirectory                  

    def pictureDirectories(self):
        if type(self.myPictureDirectories) is list:
            return self.myPictureDirectories
        else:
            return [self.myPictureDirectories]

    def verbose(self):
        return self.myVerbose

class DefaultCollection(Collection):
    def __init__(self, collectionConfig, verbose):
        self.myCollectionConfig = collectionConfig
        self.myVerbose = verbose
        self.pictureList = []
        self.myIdx = -1

    def collectionConfig(self):
        return self.myCollectionConfig

    def pictureDirectories(self):
        return self.collectionConfig().pictureDirectories()
    
    def verbose(self):
        return self.myVerbose
    
    def addPic(self, picture):
        if (self.verbose()):
            print "adding: " + picture
        self.pictureList.append(picture)

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

    def prev(self):
        if (self.myIdx - 1 > 0):
            self.myIdx = self.myIdx - 1
        else:
            self.myIdx = len(self.pictureList) - 1

        nextPic = self.pictureList[self.myIdx]
        if self.verbose():
            print "prevPic: " + nextPic

        return nextPic

class Spectacle(object):
    def __init__(self, verbose, config):
        self.dir = ""
        self.myVerbose = verbose
        self.myConfig = config  # this is a ConfigParser object
        self.myCollectionConfig = DefaultCollectionConfig(self.config(), self.verbose()) 
        self.myCollection = None
        self.mySlideShowModel = None
        self.mySlideShowView = None
        
    def config(self):
        return self.myConfig
    
    def verbose(self):
        return self.myVerbose
    
    def collectionConfig(self):
        return self.myCollectionConfig
    
    def collection(self):
        return self.myCollection
    
    def model(self):
        return self.mySlideshowModel
    
    def view(self):
        return self.mySlideShowView
    
    def controller(self):
        return self.mySlideShowController
    
    def doit(self):
        self.myCollection = DefaultCollection(self.collectionConfig(), self.verbose())
        self.myCollection.initDB();
        self.mySlideshowModel = SlideShowModel(self)
        self.mySlideShowView = PygameView(self.model())
        self.model().addListener(self.view())
        self.mySlideShowController = PygameController(self.model())
        self.controller().mainLoop()
        # self.myCollection = SimpleCollection(collectionConfig()) 
        
    def directory(self):
        return self.dir  

    def setDirectory(self, newDirectory):
        self.dir = newDirectory
        
class SlideShowModel(object):
    def __init__(self, spectacle):
        self.listeners = list()
        self.myCurrent = ""
        self.mySpectacle = spectacle
    
    def collection(self):
        return self.spectacle().collection()

    def spectacle(self):
        return self.mySpectacle
    
    def verbose(self):
        return self.spectacle().verbose()
    
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

    def quit(self):
        for listener in self.listeners:
            listener.quit()
        sys.exit()

class PygameView(SlideShowListener):
    """This abstract class is responsible for defining the interface of a SlideShowListener."""
    def __init__(self, model):
        self.myModel = model;
        self.myCurrent = ""
        self.initDisplay()
    
    def model(self):
        return self.myModel
        
    def verbose(self):
        return self.model().verbose()
        
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

    def quit(self):
        pygame.quit()

class PygameController(object):
    def __init__(self, model):
        self.myModel = model
        PygameController.TIMER_EVENT = pygame.USEREVENT + 1

    def model(self):
        return self.myModel
    
    def processKeypress(self, key):
        if key == pygame.K_LEFT:
            self.model().prev();
        elif key == pygame.K_RIGHT:
            self.model().next()
        elif key == pygame.K_ESCAPE or key == pygame.K_q:
            self.model().quit()
    
    def mainLoop(self):
        self.model().next() # display the first picture
        pygame.time.set_timer(PygameController.TIMER_EVENT, 5000)
        i = 0;
        while True:
            event = pygame.event.wait()
            if (event.type == PygameController.TIMER_EVENT):
                print "pygame.USEREVENT"
                self.model().next()
                # If we took so long another USEREVENT posted
                # we're going to clear it so that quit events
                # can make it through
                pygame.event.clear(PygameController.TIMER_EVENT)
            elif (event.type == pygame.QUIT):
                print "pygame.QUIT"
                self.model().quit()
            elif (event.type == pygame.KEYDOWN):
                print "pygame.KEYDOWN"
                self.processKeypress(event.key)
                # If the user pressed a key, clear any pending timer events
                pygame.event.clear(PygameController.TIMER_EVENT)                
            elif (i == 10):
                print "i == 10"
                pygame.quit()
                sys.exit()

            # i = i + 1
            # pygame.time.wait(100)
        
    