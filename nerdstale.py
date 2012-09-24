#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
"""
Python RPG Workshop@ FrOSCon 2012
(C) Manuel Krischer 2012

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import pygame,  math
from pygame.locals import *
from random import randint
#sound init
pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=4096)
if not pygame.mixer: print 'Warning, sound disabled'
if not pygame.font: print 'Warning, fonts disabled'
pygame.init()
"""
some helpers
"""
def findFreePos(actPos,  fieldSize):
    """
    find free pos around actPos (only level borders for now)
    """
    if actPos[0] == fieldSize[0] - 1:
        #cant drop right
        if actPos[1] == fieldSize[1] - 1:
            #cant drop down
            return [actPos[0], actPos[1]-1]
        else:
            #drop down
            return [actPos[0], actPos[1]+1]
    else:
        #drop right
        return [actPos[0]+1, actPos[1]]

def say(s):
    #dirty talking
    global msg
    msg = s
    global msgtime 
    msgtime = time  

def newPos(minY, fieldSize):
    #randomized new position
    return [randint(0, fieldSize[0]-1), randint(minY, fieldSize[1]-1)]

"""
real start
"""
#display settings
scale = 2 #factor of 32 (only 2 working right now, grapics for 1 and 4 are there
screenx = 512*scale
screeny = 396*scale
size = [screenx, screeny]
screen = pygame.display.set_mode((screenx,screeny))
pygame.display.set_caption("A Nerd's Tale")
pygame.mouse.set_visible(0)         #disable mouse cursor
pygame.key.set_repeat(100, 200)     #keyboard multiply strokerate
clock = pygame.time.Clock()
time = 0
#enviroment
imgPath = "img/"+ str(32 * scale) + "/"
sndPath = "sound/sfx/"
musPath = "sound/music/"
#field
size = 32*scale
width_field = screenx/size
height_field = screeny/size
fieldSize = [width_field,  height_field]
starty = 1
if scale < 2:
    starty += (2-scale)
if scale > 2:
    starty -= (2-scale)
#load images
#enviroment
imgStatusbar = pygame.image.load( imgPath + "statusbar.png")
imgGrass = pygame.image.load( imgPath + "grass_0.png")
imgForrest = pygame.image.load( imgPath + "forrest.png")
#enemy
imgEnemyW = pygame.image.load( imgPath + "monster.png")
imgEnemyD = pygame.image.load( imgPath + "monster_dead.png")
imgEnemyAL = pygame.image.load( imgPath + "monster_s1.png")
imgEnemyAR = pygame.image.load( imgPath + "monster_s5.png")
#player
imgPlayerL = pygame.image.load( imgPath + "hero_l.png")
imgPlayerR = pygame.image.load( imgPath + "hero_r.png")
imgPlayerDeadL = pygame.image.load( imgPath + "hero_dead_l.png")
imgPlayerDeadR = pygame.image.load( imgPath + "hero_dead_r.png")
imgPlayerSR = pygame.image.load( imgPath + "hero_s0.png")
imgPlayerSRA = pygame.image.load( imgPath + "hero_s1.png")
imgPlayerAR = (pygame.image.load( imgPath + "hero_s2.png"),
               pygame.image.load( imgPath + "hero_s3.png"), 
               pygame.image.load( imgPath + "hero_s4.png"))
imgPlayerSL = pygame.image.load( imgPath + "hero_s5.png")
imgPlayerSLA = pygame.image.load( imgPath + "hero_s6.png")
imgPlayerAL = (
               pygame.image.load( imgPath + "hero_s7.png"), 
               pygame.image.load( imgPath + "hero_s8.png"), 
               pygame.image.load( imgPath + "hero_s9.png"))
imgPlayer = imgPlayerR
#stuff
imgGold = pygame.image.load(imgPath + "gold_0.png")
imgSword = pygame.image.load(imgPath + "sword.png")
imgBlood = pygame.image.load(imgPath + "blood_0.png")
imgArmor = pygame.image.load(imgPath + "armor_01.png")
imgBottleBlue = pygame.image.load(imgPath + "bottle_blue.png")
imgBottleRed = pygame.image.load(imgPath + "bottle_red.png")
imgBottleEmpty = pygame.image.load(imgPath + "bottle_empty.png")
imgBottle = imgBottleBlue
#talk
imgBubbleL = pygame.image.load(imgPath + "bubble_l.png")
imgBubbleR = pygame.image.load(imgPath + "bubble_r.png")
imgBubble = imgBubbleL
#basic sounds http://www.freesound.org
#init sound: 48000 Hz, 2 ch, s16le
pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=4096)
#action sound
sndEnemyDie = pygame.mixer.Sound(sndPath + "enemy_die.wav")                     #
sndPlayerDie = pygame.mixer.Sound(sndPath + "player_die.wav")                   # 
sndSwordAHit = pygame.mixer.Sound(sndPath + "sword_attack_hit.wav")             # JoelAudio     cc Attribution License
sndSwordPull = pygame.mixer.Sound(sndPath + "sword_pull.wav")                   # jobro         cc Attribution License
sndSwordADef = pygame.mixer.Sound(sndPath + "sword_attack_def.wav")             # Erdie         cc Attribution License
sndClubAMiss = pygame.mixer.Sound(sndPath + "enemy_attack_club_miss.wav")       # smokebomb99       cc 0 License
sndClubAHit  = pygame.mixer.Sound(sndPath + "enemy_attack_club_hit.wav")        # Rock Savage       cc sampling+license
sndSwordAMiss = pygame.mixer.Sound(sndPath + "sword_attack_miss.wav")           # qubodup       cc 0 License
sndSwordPush = pygame.mixer.Sound(sndPath + "sword_push.wav")                   # jobro         cc Attribution License
sndWalkGrass = pygame.mixer.Sound(sndPath + "walk_grass.wav")                   # bevangoldswain    cc sampling+license
sndGoldAdd = pygame.mixer.Sound(sndPath + "gold_add.wav")                       # dobroide      cc Attribution License.
sndFoundItem = pygame.mixer.Sound(sndPath + "found_item.wav")                   # Kastenfrosch      cc 0 License
sndDrink = pygame.mixer.Sound(sndPath + "drink.wav")                            # sagetyrtle        cc 0 License
#ambience sound
pygame.mixer.music.load(musPath + "amb_outdoor.wav")                            # tsemilagain       cc sampling+license
pygame.mixer.music.play(-1)
#snd manipulation
sndWalkGrass.set_volume(0.1)
#playerstatus
energy = 3 #hitpoints to start
inv = []
gold = 0
armor = 0
level = 0
skill = 0.1     #initial skills
hitChance = 40  #chance to hit of 100
attack = (0, 1, 2, 1, 0)
aframe = 0
hasSword =  False
hasSwordReady = False
isAlive = True
lookleft = True
smoothMove = False
attacks = False
leftbubble = True
attacktime = 0
attacktimer = 80
#envstatus
enemyNear = False
enemyDead  = False
healthEmpty = False
#calculate positions
playerPos = [int(width_field/2), starty]
playerMove = [playerPos[0], playerPos[1]]
playerPosOld = [playerPos[0], playerPos[1]]
swordPos = newPos(starty, fieldSize)
armorPos = newPos(starty, fieldSize)
enemyPos = newPos(starty, fieldSize)
#calc gold positions
goldPos = []
for i in range(5):
    goldPos.append(newPos(starty, fieldSize))
#calc forrest fields
forrestPos = []
for i in range(width_field*scale, (height_field-1) * (width_field-1)):
    seed = randint(0, 100)
    if seed < 30:
        x = i % fieldSize[0]
        y = i / fieldSize[1]
        forrestPos.append([x,y])
#maybe there is a bottle of health drink
healthPos = (-1,-1)
if randint(0, 100) < 40:
    healthPos = newPos(starty, fieldSize)
#enemystatus
lastDead = (-1,-1)
killtime = 0
bloodtime = 0
killtimer = 2500
#text/font
#messagestuff
msgfont = pygame.font.Font(None, 10*scale)
msgtimer = 1400
msgtime = 0
msg = ""
#statusbar
statusfont = pygame.font.Font(None, 16)

"""
game loop
"""
run = True
while run:
    #add running time
    time += clock.get_time()
    #reset message after msgtime ticks
    if time >  msgtimer + msgtime:
        msg = ""
    #check if enemy is near - Manhattan-Metrik ( na danke, robert!!!)
    if math.fabs(enemyPos[0] - playerPos[0]) < 2 and math.fabs(enemyPos[1] - playerPos[1]) < 2:
        enemyNear = True
    else:
        enemyNear = False
    # update status text
    st_energy_txt = str(energy)
    st_armor_txt = str(armor)        
    st_gold_txt = str(gold)
    st_skill_txt = str(skill*10)
    st_day_txt = str(time/1000/60)
    st_pos_txt = str(playerPos[0]) + ", " + str(playerPos[1])
    # render status text
    st_energy = statusfont.render(st_energy_txt, True, (200,200,0))
    st_armor  = statusfont.render(st_armor_txt, True, (200,200,0))  
    st_gold   = statusfont.render(st_gold_txt, True, (200,200,0))   
    st_skill  = statusfont.render(st_skill_txt, True, (200,200,0))
    st_day    = statusfont.render(st_day_txt, True, (200,200,0))
    st_pos    = statusfont.render(st_pos_txt, True, (200,200,0))    
    #paint world
    screen.blit(imgStatusbar, (0,0))
    screen.blit(st_energy, (125, 15))
    screen.blit(st_armor, (125, 40))
    screen.blit(st_skill, (470, 15))
    screen.blit(st_pos, (470, 40))
    screen.blit(st_day, (810, 15))
    screen.blit(st_gold, (810, 40))
    #blit floor
    for x in range(0, width_field + 1):
        starty = 1      
        if scale < 2:
            starty += (2-scale)
        for y in range(starty, height_field + 1):
            screen.blit(imgGrass, (x*size,y*size))
    #forrest, river later
    for x in forrestPos:
        a,b = x
        screen.blit(imgForrest,(a*size,b*size))   
    #sword
    screen.blit(imgSword, (swordPos[0]*size, swordPos[1]*size))
    #armor
    screen.blit(imgArmor, (armorPos[0]*size, armorPos[1]*size))
    #paint enemy according to player position
    if enemyNear and isAlive:
        #prepare to attack
        if playerPos[0] > enemyPos[0]:
            imgEnemy = imgEnemyAR
        else:
            imgEnemy = imgEnemyAL
    else:
        #guarding
        imgEnemy = imgEnemyW
    
    if not time >  killtimer + killtime:
        imgEnemy = imgEnemyD
        bloodtime = time
    screen.blit(imgEnemy, (enemyPos[0]*size, enemyPos[1]*size))
    
    if enemyDead:            
        sndEnemyDie.play()
        pygame.time.delay(1000)
        enemyPos = newPos(starty, fieldSize)
        enemyDead  = False
        
        
    
    
    #blood
    if not time >  killtimer + bloodtime:        
        screen.blit(imgBlood, (lastDead[0]*size,lastDead[1]*size))
    #gold
    for x in goldPos:
        a,b = x
        screen.blit(imgGold,(a*size,b*size)) 
    #bottle
    screen.blit(imgBottle,(healthPos[0]*size, healthPos[1]*size))
    #message
    if msg != "": #don't blit empty messages        
        msgtext = msgfont.render(msg, True, (178,0,0),)
        
        if (lookleft or playerPos[0] > width_field-2) and playerPos[0] > 1:
            imgBubble = imgBubbleL
            msgPos = ((playerMove[0]-0.5)*size, (playerMove[1]-0.5)*size)
            txtPos = ((playerMove[0]-0.35)*size, (playerMove[1]-0.25)*size)
        else:
            imgBubble = imgBubbleR
            msgPos = ((playerMove[0]+0.5)*size, (playerMove[1]-0.5)*size)
            txtPos = ((playerMove[0]+0.65)*size, (playerMove[1]-0.25)*size)
        screen.blit(imgBubble, msgPos)
        screen.blit(msgtext, txtPos)
    #paint player according to action        
    if enemyNear:
        if hasSword:
            if not hasSwordReady:
                sndSwordPull.play()
                hasSwordReady = True
                
            if lookleft:
                imgPlayer = imgPlayerSLA
            else:
                imgPlayer = imgPlayerSRA
        else:
            if lookleft:
                imgPlayer = imgPlayerL
            else:
                imgPlayer = imgPlayerR
    else:
        if hasSword:
            if hasSwordReady:
                sndSwordPush.play()
                hasSwordReady = False
            if lookleft:
                imgPlayer = imgPlayerSL
            else:
                imgPlayer = imgPlayerSR
        else:
            if lookleft:
                imgPlayer = imgPlayerL
            else:
                imgPlayer = imgPlayerR
    #hey, we are dead
    if energy <= 0 and not isAlive:
        if lookleft:
            imgPlayer = imgPlayerDeadL
        else:
            imgPlayer = imgPlayerDeadR
        energy = 0
        say("R.I.P")
        screen.blit(imgPlayer, (playerMove[0]*size, playerMove[1]*size))
        sndPlayerDie.set_volume(0.5)
        sndPlayerDie.fadeout(1000)
        sndPlayerDie.play()
        pygame.time.delay(2000)
        run = False
    if not playerMove == playerPos:
        smoothMove = True       
        if playerMove[0] < playerPos[0]:
            playerMove[0] += 1/float(size/2)
        elif playerMove[0] > playerPos[0]:
            playerMove[0] -= 1/float(size/2)
        if playerMove[1] < playerPos[1]:
            playerMove[1] += 1/float(size/2)
        elif playerMove[1] > playerPos[1]:
            playerMove[1] -= 1/float(size/2)
        pygame.time.delay(2)
    else:
        smoothMove = False
    if attacks:
        if time > attacktime + attacktimer:
            #nextframe
            attacktime += attacktimer            
            print aframe,  attack[aframe]
            if aframe < 4:
                aframe += 1
            else:
                aframe = 0
                attacks = False
        
        if lookleft:
            imgPlayer = imgPlayerAL[attack[aframe]]
        else:
            imgPlayer = imgPlayerAR[attack[aframe]]

        
    #paint player
    screen.blit(imgPlayer, (playerMove[0]*size, playerMove[1]*size))

    for event in pygame.event.get():                
        if event.type == pygame.QUIT:
            run = False
            break
        #check for key press
        if event.type == pygame.KEYDOWN and isAlive and not smoothMove:
            if event.key == pygame.K_UP and playerPos[1] > 1:
                #up
                playerMove[1] = playerPos[1]
                playerPosOld[1] = playerPos[1]
                playerPos[1] -= 1
                sndWalkGrass.play()                                
            elif event.key == pygame.K_LEFT and playerPos[0] > 0:
                #left
                playerMove[0] = playerPosOld[0] = playerPos[0]
                playerPos[0] -= 1
                sndWalkGrass.play()
                lookleft  = True
            elif event.key == pygame.K_DOWN and playerPos[1] < height_field - 1:
                #down
                playerMove[1] = playerPosOld[1] = playerPos[1]
                playerPos[1] += 1
                sndWalkGrass.play()                                
            elif event.key == pygame.K_RIGHT and playerPos[0] < width_field - 1:
                #right
                playerMove[0] = playerPos[0]
                playerPosOld[0] = playerPos[0]              
                playerPos[0] += 1
                sndWalkGrass.play()
                lookleft = False
            elif event.key == pygame.K_i:
                #inventar
                print(inv)
            elif event.key == pygame.K_q and not inv == []:
                #drop sword
                swordPos = findFreePos(playerPos, fieldSize)
                inv.remove("Sword")
                say("Dropped!")
                hasSword = False
            elif event.key == pygame.K_a and "Sword" in inv:
                attacks = True
                attacktime =  time
                if enemyNear:
                    #hit or miss?
                    if randint(0, 100) < hitChance + skill:
                        sndSwordAHit.play()
                        enemyDead  = True
                        killtime = time
                        lastDead = enemyPos
                        skill += 0.1
                        say("Die!")
                    else:
                        sndSwordADef.play()
                        pygame.time.delay(300)
                else:
                    sndSwordAMiss.play()
            elif event.key == pygame.K_ESCAPE:
                #quit game
                run = False
                break
        else:
            continue
    #found sword
    if playerPos == swordPos:
        say("Nice!")
        swordPos = (-1,-1)
        sndFoundItem.play()
        inv.append("Sword")
        hasSword = True
    #found gold
    if playerPos in goldPos:
        say("Money!")
        gold += 1                
        sndGoldAdd.play()
        goldPos.remove(playerPos)
    #found armor
    if playerPos == armorPos:
        say("A Shirt")
        armorPos = (-1,-1)
        sndFoundItem.play()
        inv.append("Armor")
        armor += 5
    #found healing drink
    if playerPos == healthPos and not healthEmpty:
        say("First Aid")
        imgBottle = imgBottleEmpty
        healthEmpty = True
        energy += 3
        sndDrink.play()
        healthPos =  findFreePos(playerPos,  fieldSize)
    # hit by monster?
    if playerPos == enemyPos:
        if randint(0, 100) < hitChance:
            sndClubAHit.play()
            say("Ouch!")
            if armor >= 0.05:
                armor -= 0.1
                energy -= 0.2
            else:
                energy -= 1
        else:
            sndClubAMiss.play()
            say("Haha!")
            if armor >= 0.1:
                armor -= 0.1
        playerPos = findFreePos(enemyPos,  fieldSize)
    if energy <= 0:
            isAlive = False
    if armor <= 0 and "Armor" in inv :
        armor = 0
        inv.remove("Armor")

    pygame.display.update();
    clock.tick(60)
exit(0)
