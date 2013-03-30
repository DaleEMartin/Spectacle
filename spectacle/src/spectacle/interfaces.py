# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

class SelectionPolicy(object):
    """This abstract class is responsible for defining the policy of the slide show.
    A simple policy, for example, could pick the next picture in a Collection."""
    
    def collection(self):
        return self.myCollection
    
    def pickNext(self):
        raise NotImplementedError( "SelectionPolicy.pickNext() is not implemented" )

    def prev(self):
        raise NotImplementedError( "SelectionPolicy.prev() is not implemented" )
    
class CollectionConfig(object):
    """This abstract class is responsible for defines the interface of a CollectionConfig object."""
    def pictureDirectories(self):
        raise NotImplementedError( "CollectionConfig.pictureDirectories() is not implemented" )

class DatabaseConfig(object):
    """This abstract class is responsible for defines the interface of a DatabaseConfig object."""
    def databasePath(self):
        raise NotImplementedError("DatabaseConfig.databasePath() is not implemented")    

class Collection(object):        
    """This abstract class is responsible for defining the interface of a Collection."""

    def iter(self):
        return self;
    
    def get(self, index):
        raise NotImplementedError( "Collection.get(aIndex) is not implemented" )

    def __iter__(self):
        return self

    def next(self):
        raise NotImplementedError( "Collection.next() is not implemented" )
  
    def prev(self):
        raise NotImplementedError( "Collection.prev() is not implemented" )      

class SlideShowListener(object):        
    """This abstract class is responsible for defining the interface of a SlideShowListener."""
    def __init__(self):
        pass
        
    def current(self):
        raise NotImplementedError( "SlideShowListener.current() not implemented" )
    
    def setCurrent(self, newCurrent):
        raise NotImplementedError( "SlideShowListener.setCurrent() not implemented" )
