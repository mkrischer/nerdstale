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

pygame.init()
screenx = 1152
screeny = 768
size = [screenx, screeny]

screen = pygame.display.set_mode((screenx,screeny))
clock = pygame.time.Clock()

#status
inv = []
energy = 3 #hitpoints to start

path = "bilder/64/"

imgFloor = pygame.image.load( path + "grass_0.png")
imgWood = pygame.image.load( path + "forrest.png")
imgEnemyW = pygame.image.load( path + "monster.png")
imgEnemyAL = pygame.image.load( path + "monster_s1.png")
imgEnemyAR = pygame.image.load( path + "monster_s5.png")

imgPlayerL = pygame.image.load( path + "hero_l.png")
imgPlayerR = pygame.image.load( path + "hero_r.png")
imgPlayerDead = pygame.image.load( path + "hero_dead.png")

imgPlayerSR = pygame.image.load( path + "hero_s0.png")
imgPlayerSRA = pygame.image.load( path + "hero_s1.png")
imgPlayerSL = pygame.image.load( path + "hero_s5.png")
imgPlayerSLA = pygame.image.load( path + "hero_s6.png")

#imgGold = pygame.image.load( path + "gold.png")
imgSword = pygame.image.load(path + "sword.png")
imgBlood = pygame.image.load(path + "blood_0.png")
imgBubbleL= pygame.image.load(path + "bubble_l.png")
imgBubbleR = pygame.image.load(path + "bubble_r.png")


hasSword =  False
enemyNear = False
lives = True
lookleft = True

imgPlayer = imgPlayerR

fieldsize = 64
width_field = screenx/fieldsize
height_field = screeny/fieldsize

playerPos = [int(width_field/2), 0]
playerPosOld = [playerPos[0], playerPos[1]]


swordPos = [randint(0, width_field-1), randint(0, height_field-1) ]
enemyPos = [randint(0, width_field-1), randint(0, height_field-1) ]
lastDead = (-1,-1)

msgfont = pygame.font.Font(None, 15)

time = 0
msgtimer = 1400
msgtime = 0
msg = ""

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
                enemyiNear = True
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
                print "no enemies nearby"
        
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
                screen.blit(imgBubbleL, ((playerPos[0]-0.5)*fieldsize, (playerPos[1]-0.5)*fieldsize))
                screen.blit(msgtext, ((playerPos[0]-0.4)*fieldsize, (playerPos[1]-0.35)*fieldsize))

	#sword
	screen.blit(imgSword, (swordPos[0]*fieldsize, swordPos[1]*fieldsize))
	
	#paint enemy according to player position
        if enemyNear and lives:
                if playerPos[0] > enemyPos[0]:
                        imgEnemy = imgEnemyAR
                else:
                        imgEnemy = imgEnemyAL
        else:
                imgEnemy = imgEnemyW
	screen.blit(imgEnemy, (enemyPos[0]*fieldsize, enemyPos[1]*fieldsize))


        #blood        
        screen.blit(imgBlood, (lastDead[0]*fieldsize,lastDead[1]*fieldsize))

        #alte position speichern
        playerPosOld[0] = playerPos[0]
        playerPosOld[1] = playerPos[1]

        #paint player according to action        
        if enemyNear:
                if hasSword:
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
        if not lives:
                imgPlayer = imgPlayerDead

        #paint player according to action
        screen.blit(imgPlayer, (playerPos[0]*fieldsize, playerPos[1]*fieldsize))

        for event in pygame.event.get():                
                if event.type == pygame.QUIT:
                        run = False
                        break
                #check for key press

	        #tasten abfragen
        	if event.type == pygame.KEYDOWN and lives:
                        
	        	if event.key == pygame.K_UP and playerPos[1] > 0:
		        	#up
			        playerPos[1] -= 1
        		elif event.key == pygame.K_LEFT and playerPos[0] > 0:
	        		#left
		        	playerPos[0] -= 1
                                lookleft  = True
        		elif event.key == pygame.K_DOWN and playerPos[1] < height_field - 1:
	        		#down
        			playerPos[1] += 1
	        	elif event.key == pygame.K_RIGHT and playerPos[0] < width_field - 1:
		        	#right
		        	playerPos[0] += 1
                                lookleft = False
        		elif event.key == pygame.K_i:
	        		#inventar
		        	print(env)
        		elif event.key == pygame.K_q and not inv == []:
	        		#schwert fallen lassen
		        	if playerPos[0] == width_field - 1:
			        	#nicht rechts fallen lassen
				        if playerPos[1] ==height_field - 1:
        					#und nicht nach unten, also oben
	        				swordPos = [playerPos[0], playerPos[1]-1]
		        		else:
			        		#ansonsten nach unten
				        	swordPos = [playerPos[0], playerPos[1]+1]
        			else:
	        			#ansonsten nach rechts
		        		swordPos = [playerPos[0]+1, playerPos[1]]
        			inv.remove("Sword")
                                msg = "Abgelegt!"
                                msgtime = time

        			hasSword = False
	        	elif event.key == pygame.K_a and "Sword" in inv and enemyNear:
		        	lastDead = enemyPos
                                enemyPos = (-1,-1)
                                msg = "Stiiiirb!"
                                msgtime = time
		        	enemyPos = [randint(0, width_field-1), randint(0, height_field-1) ]			
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

	# hit Monster?
	if playerPos == enemyPos:
                msg = "Aua"
                msgtime = time                
		energy -= 1
		playerPos[0] = playerPosOld[0]
                playerPos[1] = playerPosOld[1]
	
	#quit if dead
	if energy == 0:
                msg = "R.I.P"
                msgtime = time
		lives = False
        pygame.display.update();
        clock.tick(100)
exit(0)

