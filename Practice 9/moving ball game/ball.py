import pygame

class RedBall:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.radius = 25
        self.color = (255, 0, 0)
        self.speed_x = 20
        self.speed_y = 20
    def up(self):
        if self.y - self.radius > 0:
            self.y -= self.speed_y
    def down(self):
        if self.y + self.radius < 600:
            self.y += self.speed_y
    def left(self): 
        if self.x - self.radius > 0:
            self.x -= self.speed_x
    def right(self):
        if self.x + self.radius < 900:
            self.x += self.speed_x
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
