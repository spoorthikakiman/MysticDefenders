import pygame
import random
import math
from pygame import mixer
#Initialise game
pygame.init()
clock = pygame.time.Clock()
# Create screen
screen = pygame.display.set_mode((800,600))


#background
mixer.music.load('city-bgm-336601.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Mystic Defenders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('magician.png')
playerImg = pygame.transform.smoothscale(playerImg,(80,80))
playerX = 370
playerY = 490
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('skull.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(30,130))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#sword
#ready - cant see the sword
#fire -  sword is currently moving
swordImg = pygame.image.load('sword.png')
swordX = 0
swordY = 490
swordX_change = 0
swordY_change = 0.5
sword_state = "ready"

#score part
score_value = 0
font = pygame.font.Font('Muocas Display Serif.otf',32)
textx = 10
texty = 10

#game over
over_font = pygame.font.Font('Muocas Display Serif.otf',64)
def game_over_text():
    game_over = over_font.render("GAME OVERRR <3", True,(87,49,110))
    screen.blit(game_over,(190,250))

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(87,49,110))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_sword(x,y):
    global  sword_state
    sword_state = "fire"
    screen.blit(swordImg,(x + 16,y + 10))

def isCollision(enemyX, enemyY, swordX, swordY):
    distance = math.sqrt((math.pow(enemyX-swordX,2)) + (math.pow(enemyY - swordY,2)))
    if distance < 40:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # RGB for screen color
    screen.fill((201, 163, 214))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if sword_state == "ready" :
                    sword_sound = mixer.Sound('shooting.wav')
                    sword_sound.play()
                    swordX = playerX
                    fire_sword(swordX,swordY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Player boundary
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #enemy boundary
    for i in range(num_of_enemies):
        #game over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # collision his
        collision = isCollision(enemyX[i], enemyY[i], swordX, swordY)
        if collision:
            kill_sound = mixer.Sound('kill.wav')
            kill_sound.play()
            swordY = 490
            sword_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(30, 130)
        enemy(enemyX[i], enemyY[i], i)

    #sword movement
    if sword_state == "fire" :
        fire_sword(swordX,swordY)
        swordY -= swordY_change
    if swordY <= 0 :
        sword_state = "ready"
        swordY = 480


    player(playerX,playerY)
    show_score(textx,texty)
    pygame.display.update()
