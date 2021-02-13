import math
import pygame
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('project.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('devil.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(.3)
    enemyY_change.append(50)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"  # Ready - You can't see the bullet on the screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # Fire - The bullet is currently moving
    screen.blit(bulletImg, (x + 20, y + 10))


# Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 24:
        return True
    else:
        return False


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32) # Font created
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game Over method and variables
over_font = pygame.font.Font('freesansbold.ttf', 64) # Font created

def game_over_text():
    game_over = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(game_over, (200, 250))

# Game loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((255, 255, 255))
    # Setting background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerX_change = -.5
            if event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed")
                playerX_change = .5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Bullet sound
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()

                    # Get the current X coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke has been released")
                playerX_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement + Enemy function calling
    for i in range(num_of_enemies):

        # Game over process
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = .3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling the functions
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
