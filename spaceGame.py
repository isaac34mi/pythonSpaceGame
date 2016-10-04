print("you are about to play the funniest game in the world lol!!")
print("when the enemy by pass you and touches the groud you lose")
print("when you are able to kill all enemies and the score get to 12, you win")
print("Use the ARROW KEYS to move and SPACE KEY to shoot")
print("Watch out for part 2")
import pygame
from pygame.locals import *
import random

n = 0
e = 20
done = False 
speed = 20
espeed = 2
text_2 = False
text_3 = False

# ---- Globals and setup ----
red   = (255,  0,  0)
blue  = (  0,  0,255)
white = (255,255,255)

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("icon.jpeg")
        self.rect = self.image.get_rect()


    
class Bullet(pygame.sprite.Sprite):
    "Just like Sprite only it can kill things."
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.headedRight = True
        self.image = pygame.Surface([5, 5])
        self.image.fill(blue)
        self.rect = self.image.get_rect()


class Enemy(pygame.sprite.Sprite):
    "Just like Sprite only it wants to kill you."
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.headedRight = True
        self.image = pygame.Surface([20, 20])
        self.image.fill(red)
        self.rect = self.image.get_rect()


# ---- Functions ----
def checkEvents():
    global done
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # user clicked close box
            print("User asked to quit.")
            done = True    
    
def pollKeys():
    global hero, done, pew_sound
    keys = pygame.key.get_pressed()
    if keys[K_SPACE]:
        pew_sound.play()
        createBullet()
    if keys[K_ESCAPE]:
        done = True

def createBullet():
    global hero
    bullet = Bullet()
    bullet.rect.x = hero.rect.x -5
    bullet.rect.y = hero.rect.y
    bullets.add(bullet)

def moveBullets():
    global bullets, enemies
    bulletsToRemove = []
    for bullet in bullets:        
        bullet.rect.y -= 5

        enemiesHitList = pygame.sprite.spritecollide(bullet, enemies, True)
        for enemy in enemiesHitList:
            enemies.remove(enemy)
        if len(enemiesHitList) > 0:
            bulletsToRemove.append(bullet) # This bullet needs removed, too.

    for bullet in bulletsToRemove:
        bullets.remove(bullet)
            
def createEnemy():
    for i in range(e):
        enemy = Enemy()
        enemy.rect.x = random.randrange(0,650)
        enemy.rect.y = random.randrange(100)
        enemy.headingRight = False
        enemies.add(enemy)


def moveEnemies():
    for enemy in enemies:
        enemy.rect.y += espeed
        

##main
width = 700
height = 900

##game spirit
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
heroes = pygame.sprite.Group()

hero = Hero()
heroes.add(hero)
hero.rect.x = 280
hero.rect.y = 630

# Make enemies
if len(enemies)== 0:
    createEnemy()

pygame.init()
pew_sound = pygame.mixer.Sound("pew.wav")
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("The space Game I")
keys = [False, False, False, False,]
herostand =[280,630]
# images
#hero = pygame.image.load("gametool/images/icon.jpeg")
backG = pygame.image.load("stars.jpg")
##backGsound = pygame.mixer.Sound("moonlight.wav")
music2= pygame.mixer.music.load("pac_die.wav")


##font = pygame.font.Font(None, 36)
##text = font.render("score:%d"%n, True,white)
##screen.blit(text,[0,0])
#### 
clock = pygame.time.Clock()
music1=pygame.mixer.music.load("pac_intro.wav")
music1= pygame.mixer.music.play(-1)

# - keep looping through
while done == False:
    
    #  - events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==K_LEFT:
                keys[0]=True
            elif event.key==K_UP:
                keys[1]=True
            elif event.key==K_RIGHT:
                keys[2]=True
            elif event.key==K_DOWN:
                keys[3]=True
##            elif event.key==k_SPACE:
##                keys[4]=True
####                createBullet()
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                keys[0]=False
            elif event.key==pygame.K_UP:
                keys[1]=False
            elif event.key==pygame.K_RIGHT:
                keys[2]=False
            elif event.key==pygame.K_DOWN:
                keys[3]=False
##            elif event.key==pygame.K_SPACE:
##                keys[4]=False
            
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0)
    if keys[0]:
        if hero.rect.x > 0: 
            hero.rect.x-=speed
    elif keys[2]:
        if hero.rect.x < 650:
            hero.rect.x+=speed
    if keys[1]:
        if hero.rect.y > 0:
            hero.rect.y-=speed
    elif keys[3]:
        if hero.rect.y < 650:
            hero.rect.y+=speed
   
        
    if len(enemies)== 0:
        n = n+1
        espeed = espeed + 1
        e = e+1 
        createEnemy()
    moveEnemies()
    moveBullets()
    pollKeys()

    for enemy in enemies:
        if enemy.rect.y> 700:
            done = True
            text_2 = True 

            #music2 = pygame.mixer.music.play()
            
    if n == 12:
        done = True
        text_3 = True
        
        
            
#   clear the screen before drawing it again
    screen.fill(0)
    #  - draw the screen elements
    for x in range(width/backG.get_width()+1):
        for y in range(height/backG.get_height()+1):
            screen.blit(backG,(x*200,y*100))
            
    enemies.draw(screen)
    bullets.draw(screen)
    heroes.draw(screen)

##    backGsound.play(-1)

    font = pygame.font.Font(None, 36)
    text = font.render("score:%d"%n, 1,white)
    screen.blit(text,[0,0])
    if text_2:
        font = pygame.font.Font(None, 100)
        text2 =font.render("you lose", 1,white)
        screen.blit(text2,[300,200])
    if text_3:
        font = pygame.font.Font(None, 60)
        text2 =font.render("you win!!yeaaa", 1,white)
        screen.blit(text2,[300,200])
        

    #   update the screen
    pygame.display.flip()
    clock.tick(20)
pygame.quit()
