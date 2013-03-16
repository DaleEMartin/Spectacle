class Spectacle(object):
#    def __init__(self, initial_balance=0):
#        self.balance = initial_balance
    def __init__(self):
        self.dir = ""
        
    def directory(self):
        return self.dir  

    def setDirectory(self, newDirectory):
        self.dir = newDirectory
        
class SelectionPolicy(object):
    """This abstract class is responsible for defining the policy of the slide show.
    A simple policy, for example, could pick the next picture in a Collection."""
    def __init__(self, aCollection):
        self.myCollection = aCollection;
    
    def collection(self):
        return self.myCollection
    
    def pickNext(self):
        raise NotImplementedError( "SelectionPolicy.pickNext() is not implemented" )

    def prev(self):
        raise NotImplementedError( "SelectionPolicy.prev() is not implemented" )
        
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
    