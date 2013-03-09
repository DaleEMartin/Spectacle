class Spectacle(object):
#    def __init__(self, initial_balance=0):
#        self.balance = initial_balance
    def __init__(self):
        self.dir = ""
        
    def directory(self):
        return self.dir  

    def setDirectory(self, newDirectory):
        self.dir = newDirectory