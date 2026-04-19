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
    # Фон основной игры
    background = pygame.image.load("background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Экран смерти (Твой JPEG файл)
    skyrim_img = pygame.image.load("skyrim_death.jpg").convert()
    skyrim_img = pygame.transform.scale(skyrim_img, (WIDTH, HEIGHT))

    # Твои MP3 звуки
    eat_sound = pygame.mixer.Sound("eat.mp3")
    death_sound = pygame.mixer.Sound("death.mp3")
    
except Exception as e:
    print(f"Брат, какой-то косяк с файлами: {e}")
    print("Проверь, что background.png, skyrim_death.jpeg, eat.mp3 и death.mp3 на месте!")
    pygame.quit()
    sys.exit()

# --- ЦВЕТА ---
RED = (255, 0, 0)
DARK_RED = (180, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- ШРИФТ ---
font = pygame.font.SysFont("Arial", 30, bold=True)

# --- ПЕРЕМЕННЫЕ ИГРЫ ---
snake = [(100, 100), (80, 100), (60, 100)]
dx, dy = CELL, 0
score = 0
speed = 7
FOOD_LIFETIME = 5

# --- ФУНКЦИЯ ЭКРАНА СМЕРТИ ---
def show_death_screen():
    # 1. Сразу бахаем звук ФААААА
    death_sound.play()
    
    # 2. Выводим картинку смерти
    screen.blit(skyrim_img, (0, 0))
    pygame.display.update()
    
    # 3. Держим экран 4 секунды, чтобы звук успел проиграться
    time.sleep(4)

# --- ГЕНЕРАЦИЯ ЕДЫ ---
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake:
            weight = random.choice([1, 2, 5])
            if weight == 1:
                color = (0, 200, 0) # Обычная
            elif weight == 2:
                color = (255, 165, 0) # Вкусная
            else:
                color = (255, 0, 0) # Эпическая
            return {
                "pos": (x, y),
                "weight": weight,
                "color": color,
                "time": time.time()
            }

food = generate_food()

# --- ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ ---
running = True
while running:
    # 1. Управление
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

    # 2. Движение головы
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # 3. Проверка на смерть (Границы или Сами себя)
    if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT) or new_head in snake:
        show_death_screen()
        running = False
        continue

    snake.insert(0, new_head)

    # 4. Проверка на хавчик
    if new_head == food["pos"]:
        score += food["weight"]
        eat_sound.play() # Твой звук поедания
        food = generate_food()
    else:
        snake.pop()

    # 5. Срок годности еды
    if time.time() - food["time"] > FOOD_LIFETIME:
        food = generate_food()

    # 6. Отрисовка всего на экран
    screen.blit(background, (0, 0)) # Рисуем фон

    # Рисуем змею (голова темнее, хвост светлее)
    for i, segment in enumerate(snake):
        current_color = DARK_RED if i == 0 else RED
        pygame.draw.rect(screen, current_color, (segment[0], segment[1], CELL - 1, CELL - 1))

    # Рисуем еду
    pygame.draw.rect(screen, food["color"], (food["pos"][0], food["pos"][1], CELL, CELL))

    # Выводим счет
    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (15, 15))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()