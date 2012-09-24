import os,  pygame

class Item(object): 
    """
    general item
    """
    def __init__(self,  name,  block=False, collectable=False,  img=pygame.Surface): 
        self.__id = os.urandom(32)
        self.__name = name
        self.__desc = ""
        self.__weight = 0
        self.__block = block
        self.__img = img
        self.__collectable = collectable
    
    
    def getID(self):
        return self.__id

    def getName(self):
        return self.__name
        
    def getBlock(self):
        return self.__block

    def getWeigth(self):
        return self.__weigth
    
    def getImg(self):
        return  self.__img
    
    def setImg(self,  img):
        self.__img = img
    
    def setName(self,  name):
        self.__name = str(name)
    
    def setBlock(self, status):
        self.__block = status
    
    def setWeight(self, weigth):
        self.__weigth = weigth
    


class goldCoin(Item):
    """
    representation of gold coin
    """
    __weight = 0.0
    __value  = 1
    
    
class goldBag(Item):
    """
    representation of gold bag
    """
    __weight = 0.0
    __value = 10

class firstAid(Item):
    """
    representation of heal drink
    """
    __weight = 0.5
    __value = 5
