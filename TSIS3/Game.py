import pygame
import sys
import json
import random
import time
from pygame.locals import *

pygame.init()

# ---------------- WINDOW ---------------- #
FPS = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# ---------------- COLORS ---------------- #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 120, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# ---------------- FONTS ---------------- #
big_font = pygame.font.SysFont("Verdana", 40)
font = pygame.font.SysFont("Verdana", 25)
small_font = pygame.font.SysFont("Verdana", 18)

# ---------------- FILES ---------------- #
SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

# ---------------- SETTINGS ---------------- #
def default_settings():
    return {
        "sound": True,
        "car_color": "red",
        "difficulty": "medium"
    }

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = default_settings()
        save_settings(data)

    defaults = default_settings()
    for key, value in defaults.items():
        if key not in data:
            data[key] = value
    return data

settings = load_settings()

# ---------------- LEADERBOARD ---------------- #
def load_scores():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_score(name, score_value, distance_value):
    scores = load_scores()
    scores.append({
        "name": name,
        "score": int(score_value),
        "distance": int(distance_value)
    })
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f, indent=4)

# ---------------- ASSETS ---------------- #
background = pygame.image.load("AnimatedStreet.png").convert()
enemy_img = pygame.image.load("Enemy.png").convert_alpha()
coin_img = pygame.image.load("Coin.png").convert_alpha()
oil_img = pygame.image.load("oil.png").convert_alpha()
shield_img = pygame.image.load("shield.png").convert_alpha()
repair_img = pygame.image.load("repair.png").convert_alpha()
nitro_img = pygame.image.load("nitro.png").convert_alpha()
background_music = pygame.mixer.Sound("background.wav")
pygame.mixer.Sound.set_volume(background_music, 0.2)
background_music.play(-1)

player_red = pygame.image.load("Player_red.png").convert_alpha()
player_blue = pygame.image.load("Player_blue.png").convert_alpha()
player_white = pygame.image.load("Player_white.png").convert_alpha()
player_yellow = pygame.image.load("Player_yellow.png").convert_alpha()

try:
    crash_sound = pygame.mixer.Sound("crash.wav")
except:
    crash_sound = None

# ---------------- HELPERS ---------------- #
def play_sound(sound):
    if settings["sound"] and sound is not None:
        sound.play()

def get_player_image():
    if settings["car_color"] == "red":
        return player_red
    elif settings["car_color"] == "blue":
        return player_blue
    elif settings["car_color"] == "white":
        return player_white
    elif settings["car_color"] == "yellow":
        return player_yellow
    return player_red

def get_difficulty_values():
    if settings["difficulty"] == "easy":
        return {
            "base_speed": 4,
            "enemy_spawn": 1700,
            "coin_spawn": 1800,
            "oil_spawn": 3000,
            "speed_inc": 3500
        }
    elif settings["difficulty"] == "hard":
        return {
            "base_speed": 6,
            "enemy_spawn": 1000,
            "coin_spawn": 1600,
            "oil_spawn": 2000,
            "speed_inc": 2200
        }
    return {
        "base_speed": 5,
        "enemy_spawn": 1400,
        "coin_spawn": 1800,
        "oil_spawn": 2500,
        "speed_inc": 3000
    }

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, GRAY, (x, y, w, h))
    pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h), 2)
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, label_rect)
    return pygame.Rect(x, y, w, h)

def draw_setting_row(title, value, y):
    screen.blit(font.render(title, True, BLACK), (40, y))
    screen.blit(font.render(str(value), True, BLUE), (150, y))
    left_btn = draw_button("<", 270, y - 5, 40, 40)
    right_btn = draw_button(">", 320, y - 5, 40, 40)
    return left_btn, right_btn

# ---------------- GAME VARIABLES ---------------- #
difficulty_values = get_difficulty_values()
BASE_SPEED = difficulty_values["base_speed"]
speed = BASE_SPEED
score = 0
coin_score = 0
distance = 0
hp = 3
player_name = ""

shield_active = False
shield_timer = 0
nitro_active = False
nitro_timer = 0

game_state = "name_input"

# ---------------- SPRITES ---------------- #
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = get_player_image()
        self.rect = self.image.get_rect(center=(200, 520))

    def refresh_image(self):
        center = self.rect.center
        self.image = get_player_image()
        self.rect = self.image.get_rect(center=center)

    def update(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[K_LEFT]:
            self.rect.move_ip(-6, 0)
        if self.rect.right < SCREEN_WIDTH and keys[K_RIGHT]:
            self.rect.move_ip(6, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -100))

    def update(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))

    def update(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Oil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = oil_img
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))

    def update(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class ShieldBoost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = shield_img
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))

    def update(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class RepairBoost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = repair_img
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))

    def update(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class NitroBoost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = nitro_img
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))

    def update(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# ---------------- GROUPS ---------------- #
P1 = Player()

enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
oils = pygame.sprite.Group()
shields = pygame.sprite.Group()
repairs = pygame.sprite.Group()
nitros = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(P1)

# ---------------- EVENTS ---------------- #
SPAWN_ENEMY = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2
SPAWN_OIL = pygame.USEREVENT + 3
INC_SPEED = pygame.USEREVENT + 4
SPAWN_SHIELD = pygame.USEREVENT + 5
SPAWN_REPAIR = pygame.USEREVENT + 6
SPAWN_NITRO = pygame.USEREVENT + 7

def apply_difficulty_timers():
    values = get_difficulty_values()
    pygame.time.set_timer(SPAWN_ENEMY, values["enemy_spawn"])
    pygame.time.set_timer(SPAWN_COIN, values["coin_spawn"])
    pygame.time.set_timer(SPAWN_OIL, values["oil_spawn"])
    pygame.time.set_timer(INC_SPEED, values["speed_inc"])
    pygame.time.set_timer(SPAWN_SHIELD, 9000)
    pygame.time.set_timer(SPAWN_REPAIR, 11000)
    pygame.time.set_timer(SPAWN_NITRO, 13000)

apply_difficulty_timers()

# ---------------- RESET ---------------- #
def reset_game():
    global BASE_SPEED, speed, score, coin_score, distance, hp
    global shield_active, shield_timer, nitro_active, nitro_timer

    values = get_difficulty_values()
    BASE_SPEED = values["base_speed"]
    speed = BASE_SPEED
    score = 0
    coin_score = 0
    distance = 0
    hp = 3

    shield_active = False
    shield_timer = 0
    nitro_active = False
    nitro_timer = 0

    enemies.empty()
    coins.empty()
    oils.empty()
    shields.empty()
    repairs.empty()
    nitros.empty()
    all_sprites.empty()

    P1.refresh_image()
    P1.rect.center = (200, 520)
    all_sprites.add(P1)

    apply_difficulty_timers()

# ---------------- MAIN LOOP ---------------- #
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "name_input":
            if event.type == KEYDOWN:
                if event.key == K_RETURN and player_name.strip() != "":
                    game_state = "menu"
                elif event.key == K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 12 and event.unicode.isprintable():
                        player_name += event.unicode

        elif game_state == "menu":
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if play_btn.collidepoint((mx, my)):
                    reset_game()
                    game_state = "game"

                if lead_btn.collidepoint((mx, my)):
                    game_state = "leaderboard"

                if settings_btn.collidepoint((mx, my)):
                    game_state = "settings"

                if quit_btn.collidepoint((mx, my)):
                    pygame.quit()
                    sys.exit()

        elif game_state == "settings":
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if sound_left.collidepoint((mx, my)) or sound_right.collidepoint((mx, my)):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                if color_left.collidepoint((mx, my)):
                    colors = ["red", "blue", "white", "yellow"]
                    idx = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(idx - 1) % len(colors)]
                    save_settings(settings)
                    P1.refresh_image()

                if color_right.collidepoint((mx, my)):
                    colors = ["red", "blue" , "white", "yellow"]
                    idx = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(idx + 1) % len(colors)]
                    save_settings(settings)
                    P1.refresh_image()

                if diff_left.collidepoint((mx, my)):
                    diffs = ["easy", "medium", "hard"]
                    idx = diffs.index(settings["difficulty"])
                    settings["difficulty"] = diffs[(idx - 1) % len(diffs)]
                    save_settings(settings)
                    apply_difficulty_timers()

                if diff_right.collidepoint((mx, my)):
                    diffs = ["easy", "medium", "hard"]
                    idx = diffs.index(settings["difficulty"])
                    settings["difficulty"] = diffs[(idx + 1) % len(diffs)]
                    save_settings(settings)
                    apply_difficulty_timers()

                if back_btn.collidepoint((mx, my)):
                    game_state = "menu"

        elif game_state == "game":
            if event.type == INC_SPEED:
                BASE_SPEED = min(BASE_SPEED + 0.5, 10)

            if event.type == SPAWN_ENEMY:
                e = Enemy()
                enemies.add(e)
                all_sprites.add(e)

            if event.type == SPAWN_COIN:
                c = Coin()
                coins.add(c)
                all_sprites.add(c)

            if event.type == SPAWN_OIL:
                o = Oil()
                oils.add(o)
                all_sprites.add(o)

            if event.type == SPAWN_SHIELD:
                s = ShieldBoost()
                shields.add(s)
                all_sprites.add(s)

            if event.type == SPAWN_REPAIR:
                r = RepairBoost()
                repairs.add(r)
                all_sprites.add(r)

            if event.type == SPAWN_NITRO:
                n = NitroBoost()
                nitros.add(n)
                all_sprites.add(n)

        elif game_state == "game_over":
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if retry_btn.collidepoint((mx, my)):
                    reset_game()
                    game_state = "game"

                if menu_btn.collidepoint((mx, my)):
                    game_state = "menu"

        elif game_state == "leaderboard":
            if event.type == MOUSEBUTTONDOWN:
                game_state = "menu"

    if game_state == "name_input":
        screen.blit(big_font.render("ENTER NAME", True, BLACK), (60, 190))
        pygame.draw.rect(screen, GRAY, (90, 270, 220, 50))
        pygame.draw.rect(screen, BLACK, (90, 270, 220, 50), 2)
        screen.blit(font.render(player_name, True, RED), (100, 280))
        screen.blit(small_font.render("Press Enter to continue", True, BLACK), (105, 360))

    elif game_state == "menu":
        screen.blit(big_font.render("RACER", True, BLACK), (120, 90))
        screen.blit(small_font.render(f"Player: {player_name}", True, BLUE), (130, 145))
        screen.blit(small_font.render(f"Difficulty: {settings['difficulty']}", True, BLACK), (120, 175))
        screen.blit(small_font.render(f"Sound: {'ON' if settings['sound'] else 'OFF'}", True, BLACK), (145, 200))
        screen.blit(small_font.render(f"Car: {settings['car_color']}", True, BLACK), (150, 225))

        play_btn = draw_button("Play", 120, 260, 160, 50)
        lead_btn = draw_button("Leaderboard", 120, 325, 160, 50)
        settings_btn = draw_button("Settings", 120, 390, 160, 50)
        quit_btn = draw_button("Quit", 120, 455, 160, 50)

    elif game_state == "settings":
        screen.blit(big_font.render("SETTINGS", True, BLACK), (85, 60))

        sound_left, sound_right = draw_setting_row(
            "Sound:", "ON" if settings["sound"] else "OFF", 170
        )
        color_left, color_right = draw_setting_row(
            "Car:", settings["car_color"], 250
        )
        diff_left, diff_right = draw_setting_row(
            "Difficulty:", settings["difficulty"], 330
        )

        screen.blit(small_font.render("Car preview", True, BLACK), (150, 405))
        preview_img = get_player_image()
        preview_rect = preview_img.get_rect(center=(200, 465))
        screen.blit(preview_img, preview_rect)

        back_btn = draw_button("Back", 120, 530, 160, 45)

    elif game_state == "game":
        if nitro_active:
            speed = BASE_SPEED + 4
            if time.time() - nitro_timer > 4:
                nitro_active = False
                speed = BASE_SPEED
        else:
            speed = BASE_SPEED

        if shield_active and time.time() - shield_timer > 5:
            shield_active = False

        screen.blit(background, (0, 0))
        all_sprites.update()
        distance += speed * 0.1

        if pygame.sprite.spritecollide(P1, shields, True):
            shield_active = True
            nitro_active = False
            shield_timer = time.time()

        if pygame.sprite.spritecollide(P1, repairs, True):
            hp = min(hp + 1, 5)

        if pygame.sprite.spritecollide(P1, nitros, True):
            nitro_active = True
            shield_active = False
            nitro_timer = time.time()

        collected = pygame.sprite.spritecollide(P1, coins, True)
        if collected:
            coin_score += len(collected)

        hit_enemy = pygame.sprite.spritecollide(P1, enemies, True)
        hit_oil = pygame.sprite.spritecollide(P1, oils, True)

        if (hit_enemy or hit_oil) and not shield_active:
            hp -= 1
            play_sound(crash_sound)

        if hp <= 0:
            total_score = score + coin_score
            save_score(player_name, total_score, distance)
            game_state = "game_over"

        all_sprites.draw(screen)

        screen.blit(small_font.render(f"Score: {score}", True, BLACK), (10, 10))
        screen.blit(small_font.render(f"Coins: {coin_score}", True, BLACK), (10, 35))
        screen.blit(small_font.render(f"Distance: {int(distance)}", True, BLACK), (10, 60))
        screen.blit(small_font.render(f"HP: {hp}", True, RED), (315, 10))
        screen.blit(small_font.render(f"Diff: {settings['difficulty']}", True, BLACK), (280, 60))

        if shield_active:
            screen.blit(small_font.render("Shield", True, GREEN), (290, 35))
        elif nitro_active:
            screen.blit(small_font.render("Nitro", True, BLUE), (300, 35))
        else:
            screen.blit(small_font.render("Boost: none", True, BLACK), (250, 35))

    elif game_state == "game_over":
        final_score = score + coin_score
        screen.blit(big_font.render("GAME OVER", True, RED), (70, 180))
        screen.blit(small_font.render(f"Player: {player_name}", True, BLACK), (130, 245))
        screen.blit(small_font.render(f"Final score: {final_score}", True, BLACK), (120, 275))
        screen.blit(small_font.render(f"Distance: {int(distance)}", True, BLACK), (130, 305))

        retry_btn = draw_button("Retry", 120, 360, 160, 50)
        menu_btn = draw_button("Menu", 120, 430, 160, 50)

    elif game_state == "leaderboard":
        scores = load_scores()
        screen.blit(big_font.render("TOP 10", True, BLACK), (125, 40))

        y = 110
        for i, entry in enumerate(scores):
            line = f"{i+1}. {entry['name']}  {entry['score']}  {entry['distance']}"
            screen.blit(small_font.render(line, True, BLACK), (35, y))
            y += 35

        screen.blit(small_font.render("Click anywhere to return", True, RED), (100, 560))

    pygame.display.update()
    clock.tick(FPS)