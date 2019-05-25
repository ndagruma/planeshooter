import pygame
import time
import random

pygame.init()

display_width = 800
display_height =600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (135,206,250)

block_color = (53,115,255)

plane_width = 65
missile_width = 10

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('plane dodge')
clock = pygame.time.Clock()

plane = pygame.image.load('plane_norm.png')
plane = pygame.transform.scale(plane,(plane_width,plane_width))

plane_thrust = pygame.image.load('plane_afterburn.png')
plane_thrust = pygame.transform.scale(plane,(plane_width,plane_width))

plane_explode = pygame.image.load('plane_blow.png')
plane_explode = pygame.transform.scale(plane_explode,(plane_width,plane_width))

heli = pygame.image.load('helicopter.png')
heli = pygame.transform.scale(heli,(plane_width,plane_width))

mis = pygame.image.load('missile.png')
mis = pygame.transform.scale(mis,(missile_width ,25))

exheli = pygame.image.load('explodeheli.png')
exheli = pygame.transform.scale(exheli,(plane_width,plane_width))


cloud1 = pygame.image.load('cloud1.png')
cloud1 = pygame.transform.scale(cloud1,(100,100))

cloud2 = pygame.image.load('cloud2.png')
cloud2 = pygame.transform.scale(cloud2,(100,100))





def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))


def things_hit(count):
    display_pos_x = display_width-200
    font = pygame.font.SysFont(None, 25)
    text = font.render("Hits: "+str(count), True, black)
    gameDisplay.blit(text,(display_pos_x ,0))


def things(image, thingx, thingy, thingw, thingh, color):
    #pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    gameDisplay.blit(image, (thingx,thingy))


def clouds(image, thingx, thingy, thingw, thingh, color):
    #pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    gameDisplay.blit(image, (thingx,thingy))



def draw_missile(x,y):
    gameDisplay.blit(mis, (x,y))
    
def draw_plane_crash(x,y):
    gameDisplay.blit(plane_explode, (x,y))


def draw_heli_crash(x,y):
    gameDisplay.blit(exheli, (x,y))


def draw_plane(x,y):
    gameDisplay.blit(plane, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',60)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(1)

    game_loop()
    
def crash():
    message_display('you crashed')

    
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(blue)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)
        
        pygame.draw.rect(gameDisplay, black,(150,450,100,50))
        pygame.draw.rect(gameDisplay, red,(550,450,100,50))
        


def game_loop():
  
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    
    x_change = 0
    thing_speed_change = 0
    
    missile_speed = 0
    missile_y = y
    missile_x = (x+ plane_width/2)
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 40
    thing_height = 40
    crash_timer = 0


    cloud_startx = random.randrange(0, display_width)
    cloud_starty = -600
    cloud_speed = 3
    cloud_width = 100
    cloud_height = 100
    

    
    thingCount = 1
    
    dodged = 0
    hitcount = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            
            print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_UP:
                    thing_speed_change = 1
                elif event.key == pygame.K_DOWN:
                    thing_speed_change = -1
                elif event.key == pygame.K_SPACE:
                    missile_speed = -10 
                     
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0    
                    thing_speed_change = 0 
        
        
        x += x_change    
        thing_speed += thing_speed_change
        
        if crash_timer > 0:
            crash_timer -= 1
        if crash_timer == 1:
            thing_starty = display_height + 1
        
        if crash_timer > 0:
            thing_speed = 0
            draw_heli_crash(thing_startx,thing_starty)
        elif thing_speed > 20:
            thing_speed = 20
        elif thing_speed < 1:
            thing_speed = 1
            
        gameDisplay.fill(blue)
        
        thing_image = heli
        if crash_timer > 0:
            thing_image = exheli
        
        cloud_image = cloud1
        clouds(cloud_image,cloud_startx, cloud_starty, cloud_width, cloud_height, black)
        
        
        things(thing_image,thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        
        missile_y += missile_speed
        
        #print(missile_y)
        
        if missile_y < 0:
            missile_speed = 0
            missile_y = y
        
        if missile_speed == 0:
            missile_x = x+(plane_width/2)
        else:
            draw_missile(missile_x,missile_y)        
                    
        
        draw_plane(x,y)
        
        things_dodged(dodged)
        things_hit(hitcount)
        
        
        if x > display_width - plane_width or x < 0:
            draw_plane_crash(x,y)
            crash()
        
        if thing_starty > display_height and crash_timer == 0:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            #thing_speed += 1   
            #thing_width += (dodged * 1.2)
            thing_width = random.randrange(50,100)
            
        if y < thing_starty+thing_height and crash_timer == 0:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or \
               x+plane_width > thing_startx and x + plane_width < thing_startx+thing_width:
                print('x crossover')
                draw_plane_crash(x,y)
                crash()  

        if missile_y < thing_starty+thing_height:
            print('missile y crossover')

            if (missile_x > thing_startx and missile_x < thing_startx + thing_width or \
               missile_x+missile_width > thing_startx and missile_x + missile_width  < thing_startx+thing_width) and \
               crash_timer == 0:
                print('kill thing')
                missile_speed = 0
                missile_x = x+(plane_width/2)
                missile_y = y
                if crash_timer == 0:
                    hitcount += 1
                    dodged -= 1
                draw_heli_crash(thing_startx,thing_starty)
                crash_timer = 40
                
        pygame.display.update()
        clock.tick(60)
        

game_loop()    
pygame.quit()
quit()

