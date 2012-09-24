import os,  field,  random

class World(object):
    """
    world class, organize items and characters
    """    
    def __init__(self,  name,  worldSize=((10,5)), fieldSize=64, seed=os.urandom(32) ):
        self.__seed = seed
        self.__name = name
        self.__fields = []
        self.__worldSize = worldSize
        self.__fieldSize = fieldSize
        self.__gameWorld = self.__createWorld(self.__worldSize,  self.__fieldSize, self.__seed)
    
    def generateWorld(self, worldSize,  fieldSize,  seed):        
        """
        generate new world
        """
        random.seed(seed)
        newFieldSet = []
        for x in range(-worldSize[0]/2,  worldSize[0]/2):
            for y in range(-worldSize[1]/2,  worldSize[1]/2):
                rnd = random.randint(0, 100)
                if rnd < 5:         #5%     water?
                    type = 4
                elif rnd < 20:      #15%    desert?
                    type = 3
                elif rnd < 30:      #10%    hills
                    type = 2
                elif rnd < 50:      #20%    wood
                    type = 1
                else:               #50%    grass
                    type = 0
                nextField = field.Field( (x, y),  fieldSize,  type)
                newFieldSet.append(nextField)
                #print (nextField.getType())
        return newFieldSet
    
    def __createWorld(self,  worldSize,  fieldSize, seed):
        newWorld = { "fields" : self.generateWorld( worldSize,  fieldSize, seed )}
        return newWorld        
    
    def getFieldsize(self):
        return self.__fieldSize
        
    def getFields(self):
        if "fields" in self.__gameWorld:
            return self.__gameWorld["fields"]
        else:
            return None
    
    def getWorldsize(self):
        return self.__worldSize
        
    def getName(self):
        return self.__name
    
    def getSeed(self):
        return self.__seed
