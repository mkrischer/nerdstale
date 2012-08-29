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

import pygame, math
from pygame.locals import *
from random import randint
pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=4096)
if not pygame.mixer: print 'Warning, sound disabled'
if not pygame.font: print 'Warning, fonts disabled'



pygame.init()
screenx = 1024
screeny = 768
size = [screenx, screeny]

screen = pygame.display.set_mode((screenx,screeny))
pygame.display.set_caption("A Nerd's Tale")
pygame.mouse.set_visible(0)

clock = pygame.time.Clock()
pygame.mouse.set_cursor(*pygame.cursors.diamond)
pygame.key.set_repeat(100, 200)     #keyboard multiply strokerate

#status
inv = []
energy = 3 #hitpoints to start
gold = 0
armor = 0
level = 0
skill = 0.1

#enviroment
imgPath = "bilder/64/"
sndPath = "sound/"
fieldsize = 64
width_field = screenx/fieldsize
height_field = screeny/fieldsize

#load images
#enviroment
imgFloor = pygame.image.load( imgPath + "grass_0.png")
imgWood = pygame.image.load( imgPath + "forrest.png")

#enemy
imgEnemyW = pygame.image.load( imgPath + "monster.png")
imgEnemyAL = pygame.image.load( imgPath + "monster_s1.png")
imgEnemyAR = pygame.image.load( imgPath + "monster_s5.png")

#player
imgPlayerL = pygame.image.load( imgPath + "hero_l.png")
imgPlayerR = pygame.image.load( imgPath + "hero_r.png")
imgPlayerDeadL = pygame.image.load( imgPath + "hero_dead_l.png")
imgPlayerDeadR = pygame.image.load( imgPath + "hero_dead_r.png")
imgPlayerSR = pygame.image.load( imgPath + "hero_s0.png")
imgPlayerSRA = pygame.image.load( imgPath + "hero_s1.png")
imgPlayerSL = pygame.image.load( imgPath + "hero_s5.png")
imgPlayerSLA = pygame.image.load( imgPath + "hero_s6.png")
imgPlayer = imgPlayerR

#stuff
imgGold = pygame.image.load(imgPath + "gold_0.png")
imgSword = pygame.image.load(imgPath + "sword.png")
imgBlood = pygame.image.load(imgPath + "blood_0.png")

#talk
imgBubbleL = pygame.image.load(imgPath + "bubble_l.png")
imgBubbleR = pygame.image.load(imgPath + "bubble_r.png")
imgBubble = imgBubbleL



#basic sounds http://www.freesound.org
#init sound: 48000 Hz, 2 ch, s16le
pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=4096)

sndEnemyDie = pygame.mixer.Sound(sndPath + "enemy_die.wav")             #
sndPlayerDie = pygame.mixer.Sound(sndPath + "player_die.wav")            #
sndSwordAHit = pygame.mixer.Sound(sndPath + "sword_attack_hit.wav")      #
sndSwordPull = pygame.mixer.Sound(sndPath + "sword_pull.wav")            #
sndSwordADef = pygame.mixer.Sound(sndPath + "sword_attack_def.wav")      #
sndClubA = pygame.mixer.Sound(sndPath + "enemy_attack_club.wav")      # smokebomb99  cc 0 License
sndSwordAMiss = pygame.mixer.Sound(sndPath + "sword_attack_miss.wav")     #
sndSwordPush = pygame.mixer.Sound(sndPath + "sword_push.wav")            # jobro cc Attribution License
sndWalkGrass = pygame.mixer.Sound(sndPath + "walk_grass.wav")            # bevangoldswain cc sampling+license
sndGoldAdd = pygame.mixer.Sound(sndPath + "gold_add.wav")              # dobroide cc Attribution License.


sndWalkGrass.set_volume(0.1)

#status
hasSword =  False
enemyNear = False
isAlive = True
lookleft = True

#calculate positions
playerPos = [int(width_field/2), 0]
playerPosOld = [playerPos[0], playerPos[1]]
swordPos = [randint(0, width_field-1), randint(0, height_field-1) ]
enemyPos = [randint(0, width_field-1), randint(0, height_field-1) ]
goldPos = []
for i in range(5):
        goldPos.append([randint(0, width_field-1), randint(0, height_field-1)])

#dead
lastDead = (-1,-1)
killtime = 0
killtimer = 2500

#messagestuff
msgfont = pygame.font.Font(None, 15)
time = 0
msgtimer = 1400
msgtime = 0
msg = ""


print "gold at:"
print goldPos

##
## gogogo
##
run = True
#game loop
while run:

        time += clock.get_time()
        #reset message after msgtime ticks
        if time >  msgtimer + msgtime:
                msg = ""

        #check if enemy is near
        if enemyPos[0] == playerPos[0] and enemyPos[1] == playerPos[1]+1:
                enemyNear = True
        elif enemyPos[0] == playerPos[0] and enemyPos[1] == playerPos[1]-1:
                enemyNear = True
        elif enemyPos[1] == playerPos[1] and enemyPos[0] == playerPos[0]+1:
                enemyNear = True
                lookleft = False
        elif enemyPos[1] == playerPos[1] and enemyPos[0] == playerPos[0]-1:
                enemyNear = True
                lookleft = True
        elif enemyPos[0] == playerPos[0]+1 and enemyPos[1] == playerPos[1]+1 \
                or enemyPos[0] == playerPos[0]+1 and enemyPos[1] == playerPos[1]-1 \
                or enemyPos[0] == playerPos[0]-1 and enemyPos[1] == playerPos[1]+1 \
                or enemyPos[0] == playerPos[0]-1 and enemyPos[1] == playerPos[1]-1:
                        enemyNear = True
        elif enemyNear:
                enemyNear = False
        
	#Welt aufbauen
        #grass
	for x in range(0, width_field + 1):
		for y in range(0, height_field + 1):
			#print floor
			screen.blit(imgFloor, (x*fieldsize,y*fieldsize))

        #forrest, river later



        #message
        if msg != "": #don't blit empty messages        
                msgtext = msgfont.render(msg, True, (178,0,0),)
                if lookleft:
                        imgBubble = imgBubbleL
                        msgPos = ((playerPos[0]-0.5)*fieldsize, (playerPos[1]-0.5)*fieldsize)
                        txtPos = ((playerPos[0]-0.35)*fieldsize, (playerPos[1]-0.25)*fieldsize)
                else:
                        imgBubble = imgBubbleR
                        msgPos = ((playerPos[0]+0.5)*fieldsize, (playerPos[1]-0.5)*fieldsize)
                        txtPos = ((playerPos[0]+0.65)*fieldsize, (playerPos[1]-0.25)*fieldsize)
                screen.blit(imgBubble, msgPos)
                screen.blit(msgtext, txtPos)

	#sword
	screen.blit(imgSword, (swordPos[0]*fieldsize, swordPos[1]*fieldsize))
	
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
	screen.blit(imgEnemy, (enemyPos[0]*fieldsize, enemyPos[1]*fieldsize))


        #blood
        if not time >  killtimer + killtime:
                screen.blit(imgBlood, (lastDead[0]*fieldsize,lastDead[1]*fieldsize))

        #gold
        for x in goldPos:
                a,b = x
                screen.blit(imgGold,(a*fieldsize,b*fieldsize)) 

        #alte position speichern
        playerPosOld[0] = playerPos[0]
        playerPosOld[1] = playerPos[1]

        #paint player according to action        
        if enemyNear:
                if hasSword:
                        #sndSwordPull.play()
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
                        #sndSwordPush.play()
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
        if not isAlive:
                if lookleft:
                        imgPlayer = imgPlayerDeadL
                else:
                        imgPlayer = imgPlayerDeadR
                pygame.time.delay(2000)
                run = False

        #paint player according to action
        if playerPosOld[0] != playerPos[0]:
                i = 0
                while i < fieldsize:
                        screen.blit(imgPlayer, (playerPosOld[0]*fieldsize+i, playerPosOld[1]*fieldsize))
                        pygame.time.delay(2000)
                        i += 1
        elif playerPosOld[1] != playerPos[1]:
                i = 0
                while i < fieldsize:
                        screen.blit(imgPlayer, (playerPosOld[0]*fieldsize, playerPosOld[1]*fieldsize+i))
                        pygame.time.delay(2000)
                        i += 1
        else:
                screen.blit(imgPlayer, (playerPos[0]*fieldsize, playerPos[1]*fieldsize))


        for event in pygame.event.get():                
                if event.type == pygame.QUIT:
                        run = False
                        break
                #check for key press
        	if event.type == pygame.KEYDOWN and isAlive:
	        	if event.key == pygame.K_UP and playerPos[1] > 0:
		        	#up
			        playerPos[1] -= 1
                                sndWalkGrass.play()                                
        		elif event.key == pygame.K_LEFT and playerPos[0] > 0:
	        		#left
		        	playerPos[0] -= 1
                                sndWalkGrass.play()
                                lookleft  = True
        		elif event.key == pygame.K_DOWN and playerPos[1] < height_field - 1:
	        		#down
        			playerPos[1] += 1
                                sndWalkGrass.play()                                
	        	elif event.key == pygame.K_RIGHT and playerPos[0] < width_field - 1:
		        	#right
		        	playerPos[0] += 1
                                sndWalkGrass.play()                                
                                lookleft = False
        		elif event.key == pygame.K_i:
	        		#inventar
		        	print(inv)
        		elif event.key == pygame.K_q and not inv == []:
	        		#drop sword
		        	if playerPos[0] == width_field - 1:
			        	#cant drop right
				        if playerPos[1] == height_field - 1:
        					#cant drop down
	        				swordPos = [playerPos[0], playerPos[1]-1]
		        		else:
			        		#drop down
				        	swordPos = [playerPos[0], playerPos[1]+1]
        			else:
	        			#drop right
		        		swordPos = [playerPos[0]+1, playerPos[1]]
        			inv.remove("Sword")
                                msg = "Abgelegt!"
                                msgtime = time

        			hasSword = False
                        elif event.key == pygame.K_a and "Sword" in inv:
                                if enemyNear:
                                        sndSwordAHit.play()
                                        pygame.time.delay(300)
		        	        lastDead = enemyPos
                                        enemyPos = (-1,-1)
                                        msg = "Stiiiirb!"
                                        sndEnemyDie.play()
                                        killtime = msgtime = time
		        	        enemyPos = [randint(0, width_field-1), randint(0, height_field-1) ]
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
                msg = "HEHE!"
		msgtime = time
		swordPos = (-1,-1)
		inv.append("Sword")
		hasSword = True

        if playerPos in goldPos:
                msg = "Money!"
                msgtime = time
                gold += 1                
                print "$$$ collected"
                sndGoldAdd.play()
                goldPos.remove(playerPos)
                print goldPos                

	# hit Monster?
	if playerPos == enemyPos:
                if energy > 0:
                        msg = "Aua"                
                        msgtime = time             
		        energy -= 1
                        sndClubA.play()
                else:
                        energy = 0
                        msg = "R.I.P"
                        msgtime = time
                        isAlive = False
                        sndPlayerDie.set_volume(0.5)
                        sndPlayerDie.fadeout(1000)
                        sndPlayerDie.play()
	        playerPos[0] = playerPosOld[0]
                playerPos[1] = playerPosOld[1]
	
        pygame.display.update();
        clock.tick(60)
exit(0)

