import pygame

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
brush_size = 8   # ⭐ NEW

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# buttons
buttons = {
    "pen": pygame.Rect(10, 10, 80, 40),
    "rect": pygame.Rect(100, 10, 80, 40),
    "circle": pygame.Rect(190, 10, 80, 40),
    "eraser": pygame.Rect(280, 10, 80, 40),
}

color_buttons = {
    RED: pygame.Rect(400, 10, 40, 40),
    GREEN: pygame.Rect(450, 10, 40, 40),
    BLUE: pygame.Rect(500, 10, 40, 40),
    BLACK: pygame.Rect(550, 10, 40, 40),
}

font = pygame.font.SysFont(None, 24)

def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    
    for name, rect in buttons.items():
        pygame.draw.rect(screen, WHITE, rect)
        text = font.render(name, True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 10))
    
    for col, rect in color_buttons.items():
        pygame.draw.rect(screen, col, rect)
    
    # ⭐ show brush size
    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(size_text, (650, 20))

while True:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    draw_ui()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            # ⭐ SIZE CONTROL
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
                
                if tool == "rect":
                    pygame.draw.rect(canvas, color, (
                        start_pos[0],
                        start_pos[1],
                        end_pos[0] - start_pos[0],
                        end_pos[1] - start_pos[1]
                    ), brush_size)
                
                elif tool == "circle":
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    radius = int((dx*dx + dy*dy) ** 0.5)
                    pygame.draw.circle(canvas, color, start_pos, radius, brush_size)
            
            drawing = False
            last_pos = None
        
        if event.type == pygame.MOUSEMOTION and drawing:
            x, y = event.pos
            pos = (x, y - TOOLBAR_HEIGHT)
            
            if tool == "pen":
                if last_pos is not None:
                    pygame.draw.line(canvas, color, last_pos, pos, brush_size)
                pygame.draw.circle(canvas, color, pos, brush_size // 2)
                last_pos = pos
            
            elif tool == "eraser":
                if last_pos is not None:
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size * 2)
                pygame.draw.circle(canvas, WHITE, pos, brush_size)
                last_pos = pos
    
    pygame.display.flip()
    clock.tick(60)