import pygame
import numpy as np

pygame.init()
window = (700, 700)
screen = pygame.display.set_mode(window)
background = pygame.Surface(window)
clock = pygame.time.Clock()
running = True
dt = 0
player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (25, 25))

class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)
    def move(self, up=False, down=False, left=False, right=False):
        if right:
             self.pos.right += self.speed
        if left:
             self.pos.right -= self.speed
        if down:
             self.pos.top += self.speed
        if up:
             self.pos.top -= self.speed

p = GameObject(player, 10, 3)
while running:
    screen.blit(background, p.pos, p.pos)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        p.move(up=True)
    if keys[pygame.K_DOWN]:
        p.move(down=True)
    if keys[pygame.K_LEFT]:
        p.move(left=True)
    if keys[pygame.K_RIGHT]:
        p.move(right=True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(p.image, p.pos)
    pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
