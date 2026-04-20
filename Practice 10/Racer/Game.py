import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# Screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game variables
SPEED = 5
COIN_SPEED = 5
SCORE = 0
COIN_SCORE = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Assets
background = pygame.image.load("AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# ---------------- CLASSES ---------------- #

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def update(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def update(self):
        self.rect.move_ip(0, COIN_SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()   # remove coin


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


# ---------------- SETUP ---------------- #

P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)

# Events
INC_SPEED = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2
COIN_INC_SPEED = pygame.USEREVENT + 3

pygame.time.set_timer(INC_SPEED, 1000)
pygame.time.set_timer(SPAWN_COIN, 2000)  # spawn coin every 2 sec
pygame.time.set_timer(COIN_INC_SPEED, 4000)  # increase coin speed every 4 sec

# ---------------- GAME LOOP ---------------- #

while True:

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED = min(SPEED + 0.5, 12)  # cap speed increase
        if event.type == COIN_INC_SPEED:
            COIN_SPEED = min(COIN_SPEED + 0.5, 10)  # cap coin speed
        if event.type == SPAWN_COIN:
            if len(coins) < 3:  # limit coins
                new_coin = Coin()
                coins.add(new_coin)
                all_sprites.add(new_coin)

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update sprites
    all_sprites.update()

    # Coin collision
    collected = pygame.sprite.spritecollide(P1, coins, True)
    if collected:
        COIN_SCORE += random.randint(1, 5)  # random coin value
    if COIN_SCORE >= 25:
        SPEED = 15
    # Draw
    DISPLAYSURF.blit(background, (0, 0))

    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)

    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (280, 10))

    all_sprites.draw(DISPLAYSURF)

    # Enemy collision
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)