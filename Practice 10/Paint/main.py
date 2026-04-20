import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Paint")

clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
GRAY  = (200, 200, 200)

TOOLBAR_HEIGHT = 60

tool = "pen"
color = BLUE
drawing = False
start_pos = None
last_pos = None
brush_size = 8

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# buttons
buttons = {
    "pen": pygame.Rect(10, 10, 70, 40),
    "rect": pygame.Rect(90, 10, 70, 40),
    "circle": pygame.Rect(170, 10, 70, 40),
    "square": pygame.Rect(250, 10, 70, 40),
    "r_triangle": pygame.Rect(330, 10, 90, 40),
    "e_triangle": pygame.Rect(430, 10, 90, 40),
    "rhombus": pygame.Rect(530, 10, 80, 40),
    "eraser": pygame.Rect(620, 10, 80, 40),
}

color_buttons = {
    RED: pygame.Rect(720, 10, 30, 30),
    GREEN: pygame.Rect(760, 10, 30, 30),
    BLUE: pygame.Rect(800, 10, 30, 30),
    BLACK: pygame.Rect(840, 10, 30, 30),
}

font = pygame.font.SysFont(None, 18)

def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    
    for name, rect in buttons.items():
        pygame.draw.rect(screen, WHITE, rect)
        text = font.render(name, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 12))
    
    for col, rect in color_buttons.items():
        pygame.draw.rect(screen, col, rect)
    
    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(size_text, (10, 45))

while True:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    draw_ui()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                brush_size = min(50, brush_size + 1)
            elif event.key == pygame.K_DOWN:
                brush_size = max(1, brush_size - 1)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            if y < TOOLBAR_HEIGHT:
                for name, rect in buttons.items():
                    if rect.collidepoint(x, y):
                        tool = name
                
                for col, rect in color_buttons.items():
                    if rect.collidepoint(x, y):
                        color = col
            else:
                drawing = True
                start_pos = (x, y - TOOLBAR_HEIGHT)
                last_pos = start_pos
        
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)
                
                x1, y1 = start_pos
                x2, y2 = end_pos
                
                if tool == "rect":
                    pygame.draw.rect(canvas, color, (x1, y1, x2-x1, y2-y1), brush_size)
                
                elif tool == "square":
                    side = min(abs(x2-x1), abs(y2-y1))
                    pygame.draw.rect(canvas, color, (x1, y1, side, side), brush_size)
                
                elif tool == "circle":
                    radius = int(math.hypot(x2-x1, y2-y1))
                    pygame.draw.circle(canvas, color, start_pos, radius, brush_size)
                
                elif tool == "r_triangle":
                    points = [(x1, y1), (x2, y1), (x1, y2)]
                    pygame.draw.polygon(canvas, color, points, brush_size)
                
                elif tool == "e_triangle":
                    side = abs(x2 - x1)
                    height = int((math.sqrt(3)/2) * side)
                    points = [
                        (x1, y1),
                        (x1 + side, y1),
                        (x1 + side//2, y1 - height)
                    ]
                    pygame.draw.polygon(canvas, color, points, brush_size)
                
                elif tool == "rhombus":
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
                    pygame.draw.polygon(canvas, color, points, brush_size)
            
            drawing = False
            last_pos = None
        
        if event.type == pygame.MOUSEMOTION and drawing:
            x, y = event.pos
            pos = (x, y - TOOLBAR_HEIGHT)
            
            if tool == "pen":
                if last_pos is not None:
                    pygame.draw.line(canvas, color, last_pos, pos, brush_size)
                pygame.draw.circle(canvas, color, pos, brush_size//2)
                last_pos = pos
            
            elif tool == "eraser":
                if last_pos is not None:
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size*2)
                pygame.draw.circle(canvas, WHITE, pos, brush_size)
                last_pos = pos
    
    pygame.display.flip()
    clock.tick(60)