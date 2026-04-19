import pygame

class RedBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.radius = 25
        self.color = (255, 0, 0)

        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (25, 25), 25)

        self.rect = self.image.get_rect(center=(200, 200))

    def update(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if keys[pygame.K_a]:
                  self.rect.move_ip(-20, 0)
        if self.rect.right < 900:        
              if keys[pygame.K_d]:
                  self.rect.move_ip(20, 0)
        if self.rect.top > 0:
              if keys[pygame.K_w]:
                  self.rect.move_ip(0, -20)
        if self.rect.bottom < 600:        
              if keys[pygame.K_s]:
                  self.rect.move_ip(0, 20)