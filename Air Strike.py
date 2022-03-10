import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Air Strike")

background_img = pygame.image.load("background.png")

mixer.music.load("background.wav")
mixer.music.play(-1)

playerimg = pygame.image.load("playerimg.png")
playerX = 380
playerY = 470
player_change_X = 0

enemyimg = pygame.image.load("enemy.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(10, 100)
enemy_change_X = 5
enemy_change_Y = 50

bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 470
bullet_change_X = 0
bullet_change_Y = 12
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
fontX = 10
fontY = 10

end = pygame.font.Font("freesansbold.ttf", 70)


def game_over():
    show_end = end.render("GAME OVER", True, (255, 255, 255))
    screen.blit(show_end, (180, 250))


def background():
    screen.blit(background_img, (0, 0))


def player(x, y):
    screen.blit(playerimg, (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def enemy(x, y):
    screen.blit(enemyimg, (x, y))


def collusion(enemyX, bulletX, enemyY, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


def score():
    score_show = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score_show, (fontX, fontY))


con = True
while con:
    # rgb: red green blue
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            con = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change_X += -4

            if event.key == pygame.K_RIGHT:
                player_change_X += 4

            if event.key == pygame.K_SPACE:
                bullet(bulletX, bulletY)
                mixer.music.load("bullet.wav")
                mixer.music.play()
                bulletX = playerX

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                player_change_X = 0
                player_change_Y = 0

    playerX += player_change_X

    if enemyX <= 0:
        enemy_change_X = 5
        enemyY += enemy_change_Y
    elif enemyX >= 736:
        enemy_change_X = -5
        enemyY += enemy_change_Y

    if playerX >= 736:
        playerX = 736
    if playerX <= 0:
        playerX = 0

    enemyX += enemy_change_X

    background()

    if bulletY <= 0:
        bulletY = 470
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bullet_change_Y

    collusions = collusion(enemyX, bulletX, enemyY, bulletY)

    if collusions is True:
        mixer.music.load("explosion.wav")
        mixer.music.play()
        bulletY = 470
        enemyX = random.randint(0, 736)
        enemyY = random.randint(20, 200)
        bullet_state = "ready"
        score_value += 1

    if enemyY >= 380:
        enemyX = 1000
        playerX = 1000
        game_over()

    score()
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
