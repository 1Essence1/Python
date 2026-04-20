import pygame
import random
import time
import sys

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()
pygame.mixer.init()

# --- НАСТРОЙКИ ОКНА ---
WIDTH = 600
HEIGHT = 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake: Skyrim Edition")

clock = pygame.time.Clock()

# --- ЗАГРУЗКА РЕСУРСОВ ---
try:
    background = pygame.image.load("background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    skyrim_img = pygame.image.load("skyrim_death.jpg").convert()
    skyrim_img = pygame.transform.scale(skyrim_img, (WIDTH, HEIGHT))

    eat_sound = pygame.mixer.Sound("eat.mp3")
    death_sound = pygame.mixer.Sound("death.mp3")

except Exception as e:
    print(f"Брат, проблема с файлами: {e}")
    pygame.quit()
    sys.exit()

# --- ЦВЕТА ---
RED = (255, 0, 0)
DARK_RED = (180, 0, 0)
WHITE = (255, 255, 255)

# --- ШРИФТ ---
font = pygame.font.SysFont("Arial", 30, bold=True)

# --- ПЕРЕМЕННЫЕ ---
snake = [(100, 100), (80, 100), (60, 100)]
dx, dy = CELL, 0
score = 0
speed = 7

# --- ЭКРАН СМЕРТИ ---
def show_death_screen():
    death_sound.play()
    screen.blit(skyrim_img, (0, 0))
    pygame.display.update()
    time.sleep(4)

# --- ГЕНЕРАЦИЯ ЕДЫ ---
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:
            weight = random.choice([1, 2, 5])

            if weight == 1:
                color = (0, 200, 0)
                lifetime = 6
            elif weight == 2:
                color = (255, 165, 0)
                lifetime = 4
            else:
                color = (255, 0, 0)
                lifetime = 2

            return {
                "pos": (x, y),
                "weight": weight,
                "color": color,
                "spawn_time": time.time(),
                "lifetime": lifetime
            }

food = generate_food()

# --- ИГРОВОЙ ЦИКЛ ---
running = True
while running:
    # Управление
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL, 0

    # Движение
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Смерть
    if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT) or new_head in snake:
        show_death_screen()
        running = False
        continue

    snake.insert(0, new_head)

    # Поедание
    if new_head == food["pos"]:
        score += food["weight"]
        eat_sound.play()
        food = generate_food()
    else:
        snake.pop()

    # Исчезновение еды
    if time.time() - food["spawn_time"] > food["lifetime"]:
        food = generate_food()

    # --- ОТРИСОВКА ---
    screen.blit(background, (0, 0))

    # Змея
    for i, segment in enumerate(snake):
        color = DARK_RED if i == 0 else RED
        pygame.draw.rect(screen, color, (segment[0], segment[1], CELL - 1, CELL - 1))

    # Еда
    pygame.draw.rect(screen, food["color"], (food["pos"][0], food["pos"][1], CELL, CELL))

    # Счет
    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (15, 15))

    # --- ТАЙМЕР ЕДЫ ---
    time_left = max(0, int(food["lifetime"] - (time.time() - food["spawn_time"])))
    timer_color = (255, 0, 0) if time_left <= 2 else WHITE
    timer_surf = font.render(f"Food: {time_left}s", True, timer_color)

    screen.blit(timer_surf, (WIDTH - 160, 15))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()