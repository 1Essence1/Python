import pygame
import time
import math

pygame.init()
screen = pygame.display.set_mode((650, 650))
done = False
clock_icon = pygame.image.load('images/clock.jpg')
left_hand = pygame.image.load('images/left-hand.png')
right_hand = pygame.image.load('images/right-hand.png')
screen.fill((143, 143, 143))
clock = pygame.time.Clock()

center = (325, 325)
radius = 307

def draw_rotated(image, hand, angle):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=center)
    screen.blit(rotated, rect)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.blit(clock_icon, (18 , 18))

    t = time.localtime()
    seconds = t.tm_sec
    minutes = t.tm_min

    sec_angle = -seconds * 6
    min_angle = -(minutes * 6 + seconds * 0.1)

    draw_rotated(left_hand, 'left_hand', sec_angle)
    draw_rotated(right_hand, 'right_hand', min_angle)
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()