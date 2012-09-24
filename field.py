import math

class Field(object):
    """
    a field
    """
    def __init__(self,  pos,  size,  type=0):
        self.__pos = pos
        self.__type = type
        self.__size = size
        self.__characters = []
        self.__items = []
        
    def getType(self):
        return self.__type
    
    def getPos(self):
        return self.__pos
        
    def setType(self,  type):
        self.__type = type
        
    def addItem(self,  item):
        self.__items.append(item)
        
    def removeItem(self,  name):
        self.__items.remove(name)
        
    def getItems(self):
        return self.__items
        
    def addCharacter(self,  character):
        self.__characters.append(character)
    
    def removeCharacter(self,  name):
        self.__characters.remove(name)
    
    def getCharacters(self):
        if "characters" in self.__gameWorld:
            return self.__gameWorld["characters"]
        else:
            return None
          
            
    def getNearCharacters(self):
        """
        get a list of characters around
        """
        near = []
        for ch in self.characters:
            cx,  cy = ch.getPos()
            if math.fabs(cx- self.pos[0]) < 2 and math.fabs(cy - self.pos[1]) < 2:
                near.append(ch)
        return near
    
    def getNearItems(self):
        """
        get a list of items around
        """
        near = []
        for i in self.items:
            ix,  iy = i.getPos()
            if math.fabs(ix- self.pos[0]) < 2 and math.fabs(iy - self.pos[1]) < 2:
                near.append(i)
        return near
        

    def findFreePos(self,  fieldSize):
        """
        find free pos around actPos (only level borders for now)
        """
       
