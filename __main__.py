import pygame,  init,  world,  character
from pygame.locals import *

debug = True

def initSound():
    pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=4096)    
    return

def initVideo(fieldSize):
    print (pygame.display.get_driver())
    vInfo = pygame.display.Info()
    #screen = None
    if vInfo.hw:
        acc = True
    else:        
        acc = False
    fieldx = vInfo.current_w / fieldSize
    fieldy = vInfo.current_h / fieldSize
    print (fieldx, fieldy)
    if fieldy < fieldx/16*9:
        if debug:
            print("looks like dual screen setup...")
        screenx = fieldx * fieldSize/2
    else:
        screenx = fieldx * fieldSize
    screeny = (fieldy-4) * fieldSize
    print (screenx,  screeny)
    if debug:
        if acc:
            print (" found acc video with " )
        else:
            print (" found video with ")
    print(str(vInfo.current_w) + "x" + str(vInfo.current_h) + " px")
    screen = pygame.display.set_mode((screenx,screeny))
    pygame.display.set_caption("Nerd's Tale II")
    #print (pygame.display.Info())    
    return screen,  screenx, screeny

def initStuff():    
    pygame.mouse.set_visible(0)         #disable mouse cursor
    pygame.key.set_repeat(10, 10)     #keyboard multiply strokerate
    clock = pygame.time.Clock()
    return clock
    
def initWorld(fieldx,  fieldy,  fieldsize):
    myworld = world.World("MyWorld", ((fieldx,fieldy)), fieldsize )
    newPlayer = character.Player("Thoradin") 
    #newEnemy = character.Enemy("monster")
    #newItem  = item.Item("gold")
    
    fields = myworld.getFields()
   # for field in fields:
     #   pos = field.getPos
       # if pos[0] == player[0] and pos[1] == player[1]:
         #   field.addCharacter(newPlayer)
            
    #field.addItem(item.item("Sword"))
    #field.myworld.addItem(item.item("Shirt"))
    #for i in range (0,  2):
    #    newNPC = character.NPC("guy")
    #    myworld.addCharacter(newNPC)
    return myworld
    
def game(events, screen,  myworld):
    for event in events:
    # Wertet die Event-Warteschleife aus
        if event.type == QUIT:
            end()
            return
        elif event.type == pygame.KEYDOWN:        
            if event.key == K_ESCAPE:
                end()
                return
            elif event.key == K_f:
                pygame.display.toggle_fullscreen()                
                return        
            elif event.key == pygame.K_UP:
                world.move_up(player)             
            elif event.key == pygame.K_LEFT:
                world.move_left(player)
            elif event.key == pygame.K_DOWN:
                world.move_down(player)
            elif event.key == pygame.K_RIGHT:
                world.move_right(player)
            elif event.key == pygame.K_i:
                window.show_inv(player)
            elif event.key == pygame.K_q:
                world.drop_item(player)
            elif event.key == pygame.K_a:
                world.attack(player)
    #screen.fill()
    #sprites.update(screen)
    paintFloor(screen,  myworld)
    #sprites.draw(screen)
    pygame.display.update()

def paintFloor(screen,  gameWorld):
    fields = gameWorld.getFields()    
    dx = 0
    dy = -1
    xlast = 0
    #print(init.imgGround)
    for field in fields:        
        type = field.getType()
        fieldsize = gameWorld.getFieldsize()
        pos = field.getPos()
        if not pos[0] == xlast:
            xlast = pos[0]
            dy += 1
            dx = 0
        else:
            dx += 1
        #print (dy*fieldsize, dx*fieldsize, type,  pos)
        if type + 100 in init.imgGround:
            screen.blit(init.imgGround[type + 100], (dy * fieldsize, dx * fieldsize))   
        else:
            print("bild nich gefunden: " + str(type+100))

def paintStuff(screen,  gameWorld):
    print ("")

def end():
    exit(0)
    
def main():
    pygame.init()
    initSound()
    screen, width,  height = initVideo(init.fieldSize)    
    myworld = initWorld(width/init.fieldSize,  height/init.fieldSize, init.fieldSize)
    clock = initStuff()
    #time = 0
    #paintFloor(screen,  myworld)
    while True:   
        clock.tick(30)
        game(pygame.event.get(), screen,  myworld)
    end()
main()
