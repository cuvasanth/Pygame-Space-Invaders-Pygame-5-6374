import math
import random

import pygame
from pygame import mixer

# initialization
pygame.init()

# implementation
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Player.png')
playerX = 370
playerY = 480
player_XChange = 0

# Enemy

enemyImg = []
enemyX = []
enemyY = []
enemy_XChange = []
enemy_YChange = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemy_XChange.append(4)
    enemy_YChange.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_XChange = 4
bullet_YChange = 10
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textx = 10
texty = 10

# game over text
gameover = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = gameover.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text,(200,250))


def showscore(x, y):
    score = font.render("score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Loop
running = True
while running:

    screen.fill((0, 0, 0))

    # background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_XChange = -5
            if event.key == pygame.K_RIGHT:
                player_XChange = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_XChange = 0

    # Handle the Boundaries of the Player
    playerX += player_XChange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Handle the Boundaries of the Enemy
    for i in range(number_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
                game_over_text()
            break
        enemyX[i] += enemy_XChange[i]
        if enemyX[i] <= 0:
            enemy_XChange[i] = 4
            enemyY[i] += enemy_YChange[i]
        elif enemyX[i] >= 736:
            enemy_XChange[i] = -4
            enemyY[i] += enemy_YChange[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

        # handle the Boundary  of the Bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        bulletX = playerX
        firebullet(bulletX, bulletY)
        bulletY -= bullet_YChange

    player(playerX, playerY)
    showscore(textx, texty)
    pygame.display.update()
