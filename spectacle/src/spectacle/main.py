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
import re
# import time

from spectacle.interfaces import SlideShowListener
from spectacle.interfaces import Collection
from spectacle.interfaces import CollectionConfig
from spectacle.interfaces import DisplayConfig



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
                elif entry.lower().endswith('.jpg'):
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
            print "moving to: " + nextPic

        return nextPic

    def peekNext(self):
        idx = self.myIdx
        if (idx + 1 < len(self.pictureList)):
            idx = idx + 1
        else:
            idx = 0
            
        nextPic = self.pictureList[idx]
        if self.verbose():
            print "peeking at: " + nextPic

        return nextPic
 
    def prev(self):
        if (self.myIdx - 1 >= 0):
            self.myIdx = self.myIdx - 1
        else:
            self.myIdx = len(self.pictureList) - 1

        nextPic = self.pictureList[self.myIdx]
        if self.verbose():
            print "prevPic: " + nextPic

        return nextPic

class Spectacle(object):
    @classmethod
    def constructWithConfig(cls, verbose, config):
        collectionConfig =  DefaultCollectionConfig(config, verbose)
        displayConfig = PygameDisplayConfig.constructWithConfig(verbose, config) 
        return cls(verbose, collectionConfig, displayConfig)
    
    def __init__(self, verbose, collectionConfig, displayConfig):
        self.dir = ""
        self.myVerbose = verbose
        self.myCollectionConfig = collectionConfig
        self.myDisplayConfig = displayConfig
        self.myCollection = None
        self.mySlideShowModel = None
        self.mySlideShowView = None
        
    def verbose(self):
        return self.myVerbose
    
    def collectionConfig(self):
        return self.myCollectionConfig
    
    def displayConfig(self):
        return self.myDisplayConfig
    
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
        self.mySlideShowView = PygameDisplay(self.model(), self.displayConfig())
        self.model().addListener(self.view())
        self.mySlideShowController = PygameController(self.model(), self.displayConfig())
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
        self.myCurrent = self.collection().next()
        for listener in self.listeners:
            listener.setCurrent(self.current())
            listener.setNext(self.collection().peekNext())            
        return self.myCurrent
    
    def prev(self):
        self.myCurrent = self.collection().prev()
        for listener in self.listeners:
            listener.setCurrent(self.myCurrent)
        return self.myCurrent
    
    def current(self):
        return self.myCurrent

    def quit(self):
        for listener in self.listeners:
            listener.quit()
        sys.exit()

    def rotateCounterClockwise(self):
        if self.verbose():
            print "rotateCounterClockwise(" + self.current() + ")"
        for listener in self.listeners:
            listener.rotateCounterClockwise(self.current())
    
    def rotateClockwise(self):
        if self.verbose():
            print "rotateClockWise(" + self.current() + ")"
        for listener in self.listeners:
            listener.rotateClockwise(self.current())

    def infreq(self):
        if self.verbose():
            print "infreq(" + self.current() + ")"
        for listener in self.listeners:
            listener.infreq(self.current())

    def exclude(self):
        if self.verbose():
            print "exclude(" + self.current() + ")"
        for listener in self.listeners:
            listener.infreq(self.exclude())
        

class PygameDisplayConfig(DisplayConfig):
    """Requires the verbose"""
    def __init__(self, verbose, cacheDirectory, displayOnCommand, displayOffCommand):
        self.myVerbose = verbose
        self.myCacheDirectory = cacheDirectory
        self.myDisplayOnCommand = displayOnCommand
        self.myDisplayOffCommand = displayOffCommand
        self.myScreenHeight = None
        self.myScreenWidth = None
        self.myAutoMillis = 5000
        self.myInteractiveMillis = 20000
        self.myTickMillis = 100

    @classmethod
    def constructWithConfig(cls, verbose, configParser):
        cacheDirectory = configParser.get('Display', 'CacheDirectory')
        displayOnCommand = configParser.get('Display', 'DisplayOnCommand')
        displayOffCommand = configParser.get('Display', 'DisplayOffCommand')
        return cls(verbose, cacheDirectory, displayOnCommand, displayOffCommand)

    def cacheDirectory(self):
        return self.myCacheDirectory
    
    def displayOnCommand(self):
        return self.myDisplayOnCommand

    def displayOffCommand(self):
        return self.myDisplayOffCommand
        
    def verbose(self):
        return self.myVerbose

    def setScreenWidth(self, screenWidth):
        self.myScreenWidth = screenWidth

    def setScreenHeight(self, screenHeight):
        self.myScreenHeight = screenHeight

    def screenWidth(self):
        return self.myScreenWidth
    
    def screenHeight(self):
        return self.myScreenHeight

    def autoMillis(self):
        return self.myAutoMillis

    def interactiveMillis(self):
        return self.myInteractiveMillis
        
    def tickMillis(self):
        return self.myTickMillis


class PhotoCache(object):
    def __init__(self, model, displayConfig):
        self.myModel = model
        self.myDisplayConfig = displayConfig
        self.myDictionary = dict()
        self.initcacheDirectory()
    
    def initcacheDirectory(self):
        if not os.path.exists(self.cacheDirectory()):
            os.makedirs(self.cacheDirectory())
    
    def model(self):
        return self.myModel
    
    def displayConfig(self):
        return self.myDisplayConfig
    
    def cacheDirectory(self):
        return self.displayConfig().cacheDirectory()

    def screenWidth(self):
        return self.displayConfig().screenWidth()

    def screenHeight(self):
        return self.displayConfig().screenHeight()

    def verbose(self):
        return self.model().verbose()

    def sanitizeString(self, toSanitize):
        extension = re.search(r'([.](jpg|png|gif)$)', toSanitize, re.I|re.M)
        if extension:
            extension = extension.group(0)
            baseName = toSanitize.replace(extension, "")
        else:
            extension = ''
            baseName = toSanitize

        leadingSlashes = re.search(r'^([/]+)', baseName, re.M);
        if leadingSlashes:
            baseName = re.sub(r'^([/]+)', '', baseName)
            leadingSlashes = '/'
        else:
            leadingSlashes = ''

        parts = baseName.split("/")
        nonEmpty = list()
        for part in parts:
            if part:
                part = re.sub(r'[^\w.]', "_", part)
                nonEmpty.append(part)

        newString = nonEmpty[0]
        finalIdx = len(nonEmpty)

        for part in nonEmpty[1:finalIdx]:
            newString = newString + "/" + part
       
        retval = leadingSlashes + newString + extension.lower()
        
        return retval 

    def cacheName(self, origName):
        newName = self.sanitizeString(self.cacheDirectory()) + "/" + self.sanitizeString(origName)
        return newName

    def convertAndSave(self, image):
        pilImage = Image.open(image)
        pilConverted = pilImage.convert('RGB')

        width, height = pilConverted.size
        ratio = min(self.screenWidth()/float(width), self.screenHeight()/float(height))
        
        newWidth = int(ratio * width)
        newHeight = int(ratio * height)

        if (self.verbose()):
            print "ratio: " + str(ratio)
            print "newWidth: " + str(newWidth)
            print "newHeight: " + str(newHeight)

        newImage = pilConverted.resize([newWidth, newHeight], Image.ANTIALIAS)
        name = self.cacheName(image)
        dirname = os.path.dirname(name)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if (self.verbose()):
            print "Saving image: " + name
        newImage.save(name)
        self.myDictionary[name] = True
    
    def contains(self, image):
        path = self.cacheName(image)
        return os.path.exists(path)
    
    def fetch(self, image):
        retval = None
        try:
            retval = Image.open(self.cacheName(image))
        except (RuntimeError):
            pass
        return retval

    def prepareImage(self, image):
        if self.contains(image):
            if (self.verbose):
                print "Already have: " + image
        else:
            if (self.verbose):
                print "Do not have: " + image
            self.convertAndSave(image)
        return self.fetch(image)

class PygameDisplay(SlideShowListener):
    """This abstract class is responsible for defining the interface of a SlideShowListener."""
    def __init__(self, model, displayConfig):
        self.myModel = model;
        self.myCurrent = ""
        self.myCache = None
        self.myDisplayConfig = displayConfig
        self.initDisplay()
        self.myNextPhoto = None
    
    def nextPhoto(self):
        return self.myNextPhoto
    
    def setNextPhoto(self, nextPhoto):
        self.myNextPhoto= nextPhoto
    
    def model(self):
        return self.myModel
        
    def verbose(self):
        return self.model().verbose()
        
    def displayConfig(self):
        return self.myDisplayConfig

    def screenWidth(self):
        return self.displayConfig().screenWidth()

    def screenHeight(self):
        return self.displayConfig().screenHeight()
    
    def cache(self):
        return self.myCache
    
    def initDisplay(self):
        self.myCache = PhotoCache(self.model(), self.displayConfig())
        pygame.init()
        displayInfo = pygame.display.Info();
        
        self.displayConfig().setScreenWidth(displayInfo.current_w)
        self.displayConfig().setScreenHeight(displayInfo.current_h)

        self.myDisplay = pygame.display.set_mode((self.screenWidth(), self.screenHeight()), pygame.FULLSCREEN)
        pygame.mouse.set_visible(0)        
        pygame.time.set_timer(PygameController.TIMER_EVENT, self.displayConfig().tickMillis())

    def current(self):
        return self.myCurrent
    
    def setCurrent(self, newCurrent):
        self.myCurrent = newCurrent
        self.display(newCurrent)
        
    def display(self,collectionPath):
        while (os.path.islink(collectionPath)):
            collectionPath = os.readlink(collectionPath)
        
        try:
            cachePath = self.cache().prepareImage(collectionPath)
        
            pilString = cachePath.tostring()
            pygameImage = pygame.image.fromstring(pilString,
                                                  cachePath.size,
                                                  'RGB')
            # Black out the screen to get rid of artifacts from the
            # previous display
            self.myDisplay.fill((0, 0, 0))

            # Compute the area where we have the max height/width given our
            # aspect ratio, and then split the empty part in half to center
            # the cachePath
            scaledWidth, scaledHeight = cachePath.size
            extraHeight = self.screenHeight() - scaledHeight;
            extraWidth  = self.screenWidth() - scaledWidth;

            self.myDisplay.blit(pygameImage, (extraWidth/2, extraHeight/2))

            pygame.display.update()
        except IOError:
            if self.verbose():
                print "Error displaying cachePath:", sys.exc_info()[0]

    def setNext(self, nextPic):
        pass

    def rotateClockwise(self, toRotate):
        print "PygameDisplay.rotateClockwise called"

    def rotateCounterClockwise(self, toRotate):
        print "PygameDisplay.rotateCounterClockwise called"

    def quit(self):
        pygame.quit()

class PygameController(object):
    TIMER_EVENT = pygame.USEREVENT + 1

    def __init__(self, model, displayConfig):
        self.myModel = model
        self.myState = "STARTING"
        self.myDisplayConfig = displayConfig

    def model(self):
        return self.myModel

    def displayConfig(self):
        return self.myDisplayConfig

    def verbose(self):
        return self.model().verbose()
    
    def input(self):
        event = pygame.event.wait()
        if (event.type == PygameController.TIMER_EVENT or self.myState == "STARTING"):
            return "TIMER_EVENT"
        elif (event.type == pygame.QUIT):
            if (self.verbose()):
                print "QUIT"
            return "QUIT"
        elif (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_LEFT:
                return "PREV"
            elif event.key == pygame.K_RIGHT:
                return "NEXT"
            elif event.key == pygame.K_UP:
                return "ROTATE_COUNTER"
            elif event.key == pygame.K_DOWN:
                return "ROTATE"
            elif event.key == pygame.K_x:
                return "EXCLUDE"
            elif event.key == pygame.K_i:
                return "INFREQ"
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return "QUIT"


    
    def mainLoop(self):
        clock = pygame.time.Clock()
        lastEventTime = pygame.time.get_ticks()
        lastState = self.myState
        nextState = self.myState
        while True:
            self.myState = nextState
            currentTime = pygame.time.get_ticks()
            readInput = True
            if (self.myState == "INTERACTIVE" and lastState != "INTERACTIVE"):
                readInput = False
            
            if (readInput == True):
                currentInput = self.input()

            if (self.myState == "STARTING"):
                self.model().next() # display the first picture
                nextState = "DISPLAYING"
                lastEventTime = pygame.time.get_ticks()
            elif (self.myState ==  "DISPLAYING"):
                if (currentInput == "TIMER_EVENT"):
                    if ((currentTime - lastEventTime) > self.displayConfig().autoMillis()):
                        self.model().next()
                        lastEventTime = pygame.time.get_ticks()
                    # else just swallow it
                elif (currentInput == "QUIT"):
                    self.model().quit()
                else:
                    nextState = "INTERACTIVE"
            elif (self.myState == "INTERACTIVE"):
                if (currentInput == "TIMER_EVENT"):
                    if (currentTime - lastEventTime > self.displayConfig().interactiveMillis()):
                        nextState = "DISPLAYING"
                else:
                    lastEventTime = clock.get_rawtime()
                    # Note the passage of time
                    if (currentInput == "QUIT"):
                        self.model().quit()
                    elif (currentInput == "NEXT"):
                        self.model().next()
                        pygame.event.clear(PygameController.TIMER_EVENT)
                    elif (currentInput == "PREV"):
                        self.model().prev()
                        pygame.event.clear(PygameController.TIMER_EVENT)
                    elif (currentInput == "ROTATE_COUNTER"):
                        self.model().rotateCounterClockwise()
                    elif (currentInput == "ROTATE"):
                        self.model().rotateClockwise()
                    elif (currentInput == "EXCLUDE"):
                        self.model().exclude()
                    elif (currentInput == "INFREQ"):
                        self.model().infreq()
            lastState = self.myState
    
