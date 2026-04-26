import pygame
import math
from datetime import datetime
from collections import deque

pygame.init()

WIDTH, HEIGHT = 1000, 650
TOOLBAR_HEIGHT = 80
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
DARK_GRAY = (120, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 220, 0)
PURPLE = (160, 0, 200)

canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont(None, 22)
text_font = pygame.font.SysFont(None, 32)

tool = "pencil"
color = BLACK
brush_size = 5

drawing = False
start_pos = None
last_pos = None

text_active = False
text_pos = None
typed_text = ""

buttons = {
    "pencil": pygame.Rect(10, 10, 70, 30),
    "line": pygame.Rect(90, 10, 70, 30),
    "rect": pygame.Rect(170, 10, 70, 30),
    "circle": pygame.Rect(250, 10, 70, 30),
    "square": pygame.Rect(330, 10, 70, 30),
    "right_tri": pygame.Rect(410, 10, 90, 30),
    "eq_tri": pygame.Rect(510, 10, 80, 30),
    "rhombus": pygame.Rect(600, 10, 90, 30),
    "fill": pygame.Rect(700, 10, 60, 30),
    "text": pygame.Rect(770, 10, 60, 30),
    "eraser": pygame.Rect(840, 10, 80, 30),
}

size_buttons = {
    2: pygame.Rect(10, 45, 50, 25),
    5: pygame.Rect(70, 45, 50, 25),
    10: pygame.Rect(130, 45, 50, 25),
}

color_buttons = {
    BLACK: pygame.Rect(220, 45, 30, 25),
    RED: pygame.Rect(260, 45, 30, 25),
    GREEN: pygame.Rect(300, 45, 30, 25),
    BLUE: pygame.Rect(340, 45, 30, 25),
    YELLOW: pygame.Rect(380, 45, 30, 25),
    PURPLE: pygame.Rect(420, 45, 30, 25),
}


def canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR_HEIGHT


def draw_button(rect, text, active=False):
    pygame.draw.rect(screen, DARK_GRAY if active else WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = font.render(text, True, WHITE if active else BLACK)
    screen.blit(label, (rect.x + 5, rect.y + 7))


def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    for name, rect in buttons.items():
        draw_button(rect, name, tool == name)

    for size, rect in size_buttons.items():
        draw_button(rect, str(size), brush_size == size)

    for col, rect in color_buttons.items():
        pygame.draw.rect(screen, col, rect)
        pygame.draw.rect(screen, BLACK, rect, 3 if color == col else 1)

    info = font.render("Keys: 1/2/3 size | Ctrl+S save | Enter confirm text | Esc cancel/quit", True, BLACK)
    screen.blit(info, (500, 50))


def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


def draw_shape(surface, shape, start, end, col, size):
    x1, y1 = start
    x2, y2 = end

    if shape == "line":
        pygame.draw.line(surface, col, start, end, size)

    elif shape == "rect":
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        pygame.draw.rect(surface, col, rect, size)

    elif shape == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, col, start, radius, size)

    elif shape == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        sx = x1 if x2 >= x1 else x1 - side
        sy = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, col, (sx, sy, side, side), size)

    elif shape == "right_tri":
        points = [(x1, y1), (x2, y1), (x1, y2)]
        pygame.draw.polygon(surface, col, points, size)

    elif shape == "eq_tri":
        side = abs(x2 - x1)
        height = int((math.sqrt(3) / 2) * side)

        if y2 >= y1:
            points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 + height)]
        else:
            points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - height)]

        pygame.draw.polygon(surface, col, points, size)

    elif shape == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        dx = abs(x2 - x1) // 2
        dy = abs(y2 - y1) // 2

        points = [
            (cx, cy - dy),
            (cx + dx, cy),
            (cx, cy + dy),
            (cx - dx, cy)
        ]

        pygame.draw.polygon(surface, col, points, size)


def save_canvas():
    filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    draw_ui()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if drawing and start_pos and tool in ["line", "rect", "circle", "square", "right_tri", "eq_tri", "rhombus"]:
        if mouse_y >= TOOLBAR_HEIGHT:
            preview_pos = canvas_pos((mouse_x, mouse_y))
            preview = canvas.copy()
            draw_shape(preview, tool, start_pos, preview_pos, color, brush_size)
            screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if text_active and text_pos:
        temp_text = text_font.render(typed_text + "|", True, color)
        screen.blit(temp_text, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if event.key == pygame.K_s:
                    save_canvas()

            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            if text_active:
                if event.key == pygame.K_RETURN:
                    final_text = text_font.render(typed_text, True, color)
                    canvas.blit(final_text, text_pos)
                    text_active = False
                    typed_text = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    typed_text = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                else:
                    typed_text += event.unicode

            else:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if y < TOOLBAR_HEIGHT:
                for name, rect in buttons.items():
                    if rect.collidepoint(x, y):
                        tool = name

                for size, rect in size_buttons.items():
                    if rect.collidepoint(x, y):
                        brush_size = size

                for col, rect in color_buttons.items():
                    if rect.collidepoint(x, y):
                        color = col

            else:
                pos = canvas_pos(event.pos)

                if tool == "fill":
                    flood_fill(canvas, pos[0], pos[1], color)

                elif tool == "text":
                    text_active = True
                    text_pos = pos
                    typed_text = ""

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

        if event.type == pygame.MOUSEMOTION and drawing:
            if event.pos[1] >= TOOLBAR_HEIGHT:
                pos = canvas_pos(event.pos)

                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, pos, brush_size)
                    pygame.draw.circle(canvas, color, pos, brush_size // 2)
                    last_pos = pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size * 2)
                    pygame.draw.circle(canvas, WHITE, pos, brush_size)
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = canvas_pos(event.pos)

                if tool in ["line", "rect", "circle", "square", "right_tri", "eq_tri", "rhombus"]:
                    draw_shape(canvas, tool, start_pos, end_pos, color, brush_size)

            drawing = False
            start_pos = None
            last_pos = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()