import pygame
from ball import RedBall

pygame.init()

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()
done = False

# create sprite group
all_sprites = pygame.sprite.Group()

# create ball and add to group
ball = RedBall()
all_sprites.add(ball)

# game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # update all sprites (movement happens here)
    all_sprites.update()

    # draw everything
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(144)

pygame.quit()