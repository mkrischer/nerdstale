"""
init
"""
import pygame
from random import randint

def newPos(topLeft,  bottomRight):
    #randomized new position
    return [randint(topLeft[0], bottomRight[0]-1), randint(topLeft[1], bottomRight[1]-1)]

"""
real start
"""
#display settings
fieldSize = 64


#enviroment
imgPath = "img/"+ str(fieldSize) + "/"
sndPath = "sound/sfx/"
musPath = "sound/music/"

#load images
#enviroment
imgWindow = {}
for i in range(100, 100):
    imgWindow.update({i: pygame.image.load( imgPath + "window_" + str(i) + ".png")})

#ground
imgGround = {}
for i in range(100, 105):
    imgGround.update({i:  pygame.image.load( imgPath + "ground_" + str(i) + ".png")})
#enemy
imgEnemy = {}
for i in range(100, 103):
    imgEnemy .update({i: pygame.image.load( imgPath + "enemy_" + str(i) +".png")})
#player
imgPlayer = {}
for i in range(100,  106):
    imgPlayer.update({i: pygame.image.load( imgPath + "hero_" + str(i) + ".png")})
    
for i in range(200, 206):
    imgPlayer.update({i: pygame.image.load( imgPath + "hero_" + str(i) + ".png")})
#items
imgItem = {}
for i in range(100, 106):
    imgItem.update({i: pygame.image.load( imgPath + "item_" + str(i) + ".png")})
#stuff
imgStuff = {}
for i in range(100, 100):
    imgStuff.update({i: pygame.image.load( imgPath + "stuff_" + str(i) + ".png")})
for i in range(200, 200):
    imgStuff.update({i: pygame.image.load( imgPath + "stuff_" + str(i) + ".png")})


#basic sounds http://www.freesound.org
#init sound: 48000 Hz, 2 ch, s16le
pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=4096)
#action sound
sndEnemyDie = pygame.mixer.Sound(sndPath + "enemy_die.wav")                     #
sndPlayerDie = pygame.mixer.Sound(sndPath + "player_die.wav")                   # 
sndSwordAHit = pygame.mixer.Sound(sndPath + "sword_attack_hit.wav")             # JoelAudio         cc Attribution License
sndSwordPull = pygame.mixer.Sound(sndPath + "sword_pull.wav")                   # jobro             cc Attribution License
sndSwordADef = pygame.mixer.Sound(sndPath + "sword_attack_def.wav")             # Erdie             cc Attribution License
sndClubAMiss = pygame.mixer.Sound(sndPath + "enemy_attack_club_miss.wav")       # smokebomb99       cc 0 License
sndClubAHit  = pygame.mixer.Sound(sndPath + "enemy_attack_club_hit.wav")        # Rock Savage       cc sampling+license
sndSwordAMiss = pygame.mixer.Sound(sndPath + "sword_attack_miss.wav")           # qubodup           cc 0 License
sndSwordPush = pygame.mixer.Sound(sndPath + "sword_push.wav")                   # jobro             cc Attribution License
sndWalkGrass = pygame.mixer.Sound(sndPath + "walk_grass.wav")                   # bevangoldswain    cc sampling+license
sndGoldAdd = pygame.mixer.Sound(sndPath + "gold_add.wav")                       # dobroide          cc Attribution License.
sndFoundItem = pygame.mixer.Sound(sndPath + "found_item.wav")                   # Kastenfrosch      cc 0 License
sndDrink = pygame.mixer.Sound(sndPath + "drink.wav")                            # sagetyrtle        cc 0 License
#ambience sound
pygame.mixer.music.load(musPath + "amb_outdoor.wav")                            # tsemilagain       cc sampling+license
pygame.mixer.music.play(-1)
#snd manipulation
sndWalkGrass.set_volume(0.1)
