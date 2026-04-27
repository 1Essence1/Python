import json
import os
import random
import sys

import pygame

try:
    import db
except Exception:
    db = None

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake")
CLOCK = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial", 24, bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", 18)
BIG_FONT = pygame.font.SysFont("Arial", 42, bold=True)

ASSETS = "assets"

background = pygame.image.load(os.path.join(ASSETS, "background.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

death_img = pygame.image.load(os.path.join(ASSETS, "skyrim_death.jpg"))
death_img = pygame.transform.scale(death_img, (WIDTH, HEIGHT))

eat_sound = pygame.mixer.Sound(os.path.join(ASSETS, "eat.mp3"))
death_sound = pygame.mixer.Sound(os.path.join(ASSETS, "death.mp3"))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
DARK_RED = (120, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 140, 255)
PURPLE = (150, 80, 255)
YELLOW = (240, 220, 0)

SETTINGS_FILE = "settings.json"


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = GRAY if self.rect.collidepoint(mouse) else DARK_GRAY
        pygame.draw.rect(SCREEN, color, self.rect, border_radius=8)
        pygame.draw.rect(SCREEN, WHITE, self.rect, 2, border_radius=8)
        label = SMALL_FONT.render(self.text, True, WHITE)
        SCREEN.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def load_settings():
    default = {"snake_color": [0, 200, 0], "grid": True, "sound": True}
    if not os.path.exists(SETTINGS_FILE):
        save_settings(default)
        return default
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, value in default.items():
            data.setdefault(key, value)
        return data
    except Exception:
        return default


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def draw_text(text, font, color, x, y, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    SCREEN.blit(surf, rect)


def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(SCREEN, (25, 25, 25), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(SCREEN, (25, 25, 25), (0, y), (WIDTH, y))


def random_cell(excluded):
    while True:
        pos = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
        if pos not in excluded:
            return pos


def generate_food(snake, obstacles):
    pos = random_cell(set(snake) | set(obstacles))

    if random.random() < 0.20:
        return {
            "type": "poison",
            "pos": pos,
            "weight": 0,
            "color": DARK_RED,
            "spawn_time": pygame.time.get_ticks(),
            "lifetime": 8000
        }

    weight = random.choice([1, 2, 5])
    color = GREEN if weight == 1 else ORANGE if weight == 2 else RED
    lifetime = 6000 if weight == 1 else 4500 if weight == 2 else 3000

    return {
        "type": "normal",
        "pos": pos,
        "weight": weight,
        "color": color,
        "spawn_time": pygame.time.get_ticks(),
        "lifetime": lifetime
    }


def generate_power_up(snake, obstacles, food):
    pos = random_cell(set(snake) | set(obstacles) | {food["pos"]})
    p_type = random.choice(["speed", "slow", "shield"])
    colors = {"speed": BLUE, "slow": PURPLE, "shield": YELLOW}
    return {
        "type": p_type,
        "pos": pos,
        "color": colors[p_type],
        "spawn_time": pygame.time.get_ticks(),
        "lifetime": 8000
    }


def safe_obstacle_position(pos, snake_head):
    hx, hy = snake_head
    px, py = pos
    distance = abs(hx - px) + abs(hy - py)
    return distance >= CELL * 3


def generate_obstacles(level, snake, food_pos):
    if level < 3:
        return []

    obstacles = []
    count = min(4 + level, 14)
    excluded = set(snake) | {food_pos}
    head = snake[0]

    attempts = 0
    while len(obstacles) < count and attempts < 500:
        attempts += 1
        pos = (random.randrange(CELL, WIDTH - CELL, CELL), random.randrange(CELL, HEIGHT - CELL, CELL))
        if pos in excluded or pos in obstacles:
            continue
        if not safe_obstacle_position(pos, head):
            continue
        obstacles.append(pos)

    return obstacles


def username_screen():
    username = ""
    while True:
        SCREEN.fill(BLACK)
        draw_text("Enter username", BIG_FONT, WHITE, WIDTH // 2, 110, True)
        draw_text(username + "_", FONT, GREEN, WIDTH // 2, 190, True)
        draw_text("Press ENTER to continue", SMALL_FONT, WHITE, WIDTH // 2, 250, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()[:50]
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 15 and event.unicode.isprintable() and event.unicode not in " ;'\"":
                    username += event.unicode

        pygame.display.update()
        CLOCK.tick(FPS)


def main_menu(username):
    play_btn = Button("Play", 220, 135, 160, 40)
    lead_btn = Button("Leaderboard", 220, 185, 160, 40)
    set_btn = Button("Settings", 220, 235, 160, 40)
    quit_btn = Button("Quit", 220, 285, 160, 40)

    while True:
        SCREEN.fill(BLACK)
        draw_text("TSIS4 Snake", BIG_FONT, GREEN, WIDTH // 2, 70, True)
        draw_text(f"Player: {username}", SMALL_FONT, WHITE, WIDTH // 2, 110, True)

        for b in [play_btn, lead_btn, set_btn, quit_btn]:
            b.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if play_btn.clicked(event):
                return "play"
            if lead_btn.clicked(event):
                return "leaderboard"
            if set_btn.clicked(event):
                return "settings"
            if quit_btn.clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        CLOCK.tick(FPS)


def leaderboard_screen():
    back_btn = Button("Back", 230, 350, 140, 35)
    try:
        rows = db.get_top_scores() if db else []
    except Exception as e:
        rows = []
        error = str(e)
    else:
        error = None

    while True:
        SCREEN.fill(BLACK)
        draw_text("Leaderboard", BIG_FONT, WHITE, WIDTH // 2, 35, True)

        if error:
            draw_text("Database error:", SMALL_FONT, RED, 30, 90)
            draw_text(error[:65], SMALL_FONT, RED, 30, 120)
        else:
            draw_text("#   Username        Score   Level   Date", SMALL_FONT, GREEN, 35, 85)
            y = 120
            for i, row in enumerate(rows, start=1):
                username, score, level, date = row
                text = f"{i:<3} {username[:12]:<12} {score:<7} {level:<7} {date}"
                draw_text(text, SMALL_FONT, WHITE, 35, y)
                y += 24
            if not rows:
                draw_text("No scores yet", FONT, WHITE, WIDTH // 2, 190, True)

        back_btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_btn.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

        pygame.display.update()
        CLOCK.tick(FPS)


def settings_screen(settings):
    grid_btn = Button("Toggle Grid", 55, 130, 145, 40)
    sound_btn = Button("Toggle Sound", 230, 130, 145, 40)
    color_btn = Button("Change Color", 405, 130, 145, 40)
    save_btn = Button("Save & Back", 220, 320, 160, 40)

    colors = [[0, 200, 0], [220, 0, 0], [0, 140, 255], [240, 220, 0], [255, 120, 0]]
    color_index = 0
    if settings["snake_color"] in colors:
        color_index = colors.index(settings["snake_color"])

    while True:
        SCREEN.fill(BLACK)
        draw_text("Settings", BIG_FONT, WHITE, WIDTH // 2, 60, True)
        draw_text(f"Grid: {'ON' if settings['grid'] else 'OFF'}", SMALL_FONT, WHITE, 90, 210)
        draw_text(f"Sound: {'ON' if settings['sound'] else 'OFF'}", SMALL_FONT, WHITE, 245, 210)
        draw_text("Snake color:", SMALL_FONT, WHITE, 405, 210)
        pygame.draw.rect(SCREEN, tuple(settings["snake_color"]), (450, 240, 50, 30))

        for b in [grid_btn, sound_btn, color_btn, save_btn]:
            b.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if grid_btn.clicked(event):
                settings["grid"] = not settings["grid"]
            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]
            if color_btn.clicked(event):
                color_index = (color_index + 1) % len(colors)
                settings["snake_color"] = colors[color_index]
            if save_btn.clicked(event):
                save_settings(settings)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(settings)
                return

        pygame.display.update()
        CLOCK.tick(FPS)


def game_over_screen(username, score, level, best):
    retry_btn = Button("Retry", 190, 280, 100, 40)
    menu_btn = Button("Main Menu", 310, 280, 130, 40)

    while True:
        SCREEN.fill(BLACK)
        draw_text("Game Over", BIG_FONT, RED, WIDTH // 2, 80, True)
        draw_text(f"Score: {score}", FONT, WHITE, WIDTH // 2, 145, True)
        draw_text(f"Level reached: {level}", FONT, WHITE, WIDTH // 2, 180, True)
        draw_text(f"Personal best: {max(best, score)}", FONT, GREEN, WIDTH // 2, 215, True)

        retry_btn.draw()
        menu_btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if retry_btn.clicked(event):
                return "retry"
            if menu_btn.clicked(event):
                return "menu"

        pygame.display.update()
        CLOCK.tick(FPS)


def play_game(username, settings):
    try:
        personal_best = db.get_personal_best(username) if db else 0
    except Exception:
        personal_best = 0

    snake = [(100, 100), (80, 100), (60, 100)]
    dx, dy = CELL, 0
    score = 0
    level = 1
    base_speed = 7
    current_speed = base_speed
    obstacles = []
    food = generate_food(snake, obstacles)
    power_up = None
    power_active = None
    power_end_time = 0
    shield = False
    last_power_spawn_try = 0
    saved = False

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL, 0
                elif event.key == pygame.K_ESCAPE:
                    return "menu"

        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        collision = False
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            collision = True
        if new_head in snake:
            collision = True
        if new_head in obstacles:
            collision = True

        if collision:
            if shield:
                shield = False
                # Move snake back to safe starting point after shield saves once.
                new_head = snake[0]
            else:
                if not saved:
                    try:
                        if db:
                            db.save_result(username, score, level)
                    except Exception:
                        pass
                    saved = True
                return game_over_screen(username, score, level, personal_best)

        snake.insert(0, new_head)

        if new_head == food["pos"]:
            if food["type"] == "poison":
                for _ in range(2):
                    if len(snake) > 1:
                        snake.pop()
                if len(snake) <= 1:
                    if not saved:
                        try:
                            if db:
                                db.save_result(username, score, level)
                        except Exception:
                            pass
                        saved = True
                    return game_over_screen(username, score, level, personal_best)
            else:
                score += food["weight"]
                needed_level = score // 10 + 1
                if needed_level > level:
                    level = needed_level
                    base_speed = 7 + level - 1
                    obstacles = generate_obstacles(level, snake, food["pos"])
            food = generate_food(snake, obstacles)
        else:
            snake.pop()

        if now - food["spawn_time"] > food["lifetime"]:
            food = generate_food(snake, obstacles)

        if power_up is None and now - last_power_spawn_try > 1000:
            last_power_spawn_try = now
            if random.random() < 0.15:
                power_up = generate_power_up(snake, obstacles, food)

        if power_up and now - power_up["spawn_time"] > power_up["lifetime"]:
            power_up = None

        if power_up and new_head == power_up["pos"]:
            if power_up["type"] == "speed":
                power_active = "speed"
                power_end_time = now + 5000
            elif power_up["type"] == "slow":
                power_active = "slow"
                power_end_time = now + 5000
            elif power_up["type"] == "shield":
                shield = True
            power_up = None

        if power_active and now > power_end_time:
            power_active = None

        if power_active == "speed":
            current_speed = base_speed + 5
        elif power_active == "slow":
            current_speed = max(3, base_speed - 4)
        else:
            current_speed = base_speed

        SCREEN.fill(BLACK)
        if settings["grid"]:
            draw_grid()

        for obs in obstacles:
            pygame.draw.rect(SCREEN, GRAY, (obs[0], obs[1], CELL - 1, CELL - 1))

        pygame.draw.rect(SCREEN, food["color"], (food["pos"][0], food["pos"][1], CELL - 1, CELL - 1))

        if power_up:
            pygame.draw.rect(SCREEN, power_up["color"], (power_up["pos"][0], power_up["pos"][1], CELL - 1, CELL - 1))

        snake_color = tuple(settings["snake_color"])
        for i, seg in enumerate(snake):
            color = WHITE if i == 0 else snake_color
            pygame.draw.rect(SCREEN, color, (seg[0], seg[1], CELL - 1, CELL - 1))

        food_left = max(0, (food["lifetime"] - (now - food["spawn_time"])) // 1000)
        draw_text(f"Score: {score}", SMALL_FONT, WHITE, 10, 8)
        draw_text(f"Level: {level}", SMALL_FONT, WHITE, 120, 8)
        draw_text(f"Best: {personal_best}", SMALL_FONT, WHITE, 210, 8)
        draw_text(f"Food: {food_left}s", SMALL_FONT, WHITE, 310, 8)
        draw_text(f"Shield: {'ON' if shield else 'OFF'}", SMALL_FONT, YELLOW if shield else WHITE, 420, 8)

        if power_active:
            power_left = max(0, (power_end_time - now) // 1000)
            draw_text(f"Power: {power_active} {power_left}s", SMALL_FONT, BLUE, 10, HEIGHT - 28)

        pygame.display.update()
        CLOCK.tick(current_speed)


def main():
    settings = load_settings()

    if db:
        try:
            db.setup_database()
        except Exception as e:
            print("Database is not connected. Game will run, but leaderboard/save may not work.")
            print(e)

    username = username_screen()

    while True:
        action = main_menu(username)
        if action == "play":
            while True:
                result = play_game(username, settings)
                if result == "retry":
                    continue
                break
        elif action == "leaderboard":
            leaderboard_screen()
        elif action == "settings":
            settings_screen(settings)


if __name__ == "__main__":
    main()
