import os,  pygame

class Character(object): 
    """
    base class for player and non-player characters
    """
    def __init__(self,  name, img=pygame.Surface): 
        self.id = os.urandom(32)
        self.__name = name
        self.__desc = ""
        self.__weight = 0
        self.__health = 0
        self.__armor = 0
        self.__img = img
        self.__inv = []
        self.__isAlive = True
        self.__hitChance = 30   #chance to hit of 100
        self.__hasMeleeWeapon =  False
        self.__hasRangedWeapon = False
        self.__hasMeleeWeaponReady = False
        self.__hasRangedWeaponReady = False
        self.__level = 0
        self.__gold = 0
        self.__speed = 1
        
    def getID(self):
        return self.__id

    def getName(self):
        return self.__name
    
    def getImg(self):
        return  self.__img
    
    def setImg(self,  img):
        self.__img = img
    
    def attackMelee(self,  character):
        # lets see....
        if self.hasMeleeWeapon:
            print ("attack %s",  character.getName())
        else:
            print("Raise  your fist")
        
    def attackRanged(self,  character):
        # lets see....
        if self.hasRangedWeapon:
            print ("attack %s",  character.getName())
        else:
            print("You spit at your enemy")
        
        
        

class Player(Character):
    """
    additional player characteristics
    """
    def __init__(self, name, img=pygame.Surface):
        self.__skillUnarmed = 0.3
        self.__skillMelee = 0.2
        self.__skillRanged = 0.1
        self.__skillMagic = 0.0
        self.__skillHacking = 2.0
        self.__skillFitness = 0.2
        self.__skillSunresistance = 0.5
        self.__skillSocial = 0.3
    

class Enemy(Character):    
    """
    additional enemy characteristics
    """
    def __init__(self, name, img=pygame.Surface, active=True ):
        self.__activeChasing = active


class NPC(Character):
    """
    additional npc characteristics
    """
    def __init__(self, name, img=pygame.Surface, friendly=True, helpful=False):
        self.__friendly = friendly
        self.__helpful = helpful
