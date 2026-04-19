import pygame
from ball import RedBall

pygame.init()
screen = pygame.display.set_mode((900 , 600))
ball = RedBall()
done = False
clock = pygame.time.Clock()

while not done:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            ball.up()
        if keys[pygame.K_s]:
            ball.down()
        if keys[pygame.K_a]:
            ball.left()
        if keys[pygame.K_d]:
            ball.right()
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(144)
pygame.quit()