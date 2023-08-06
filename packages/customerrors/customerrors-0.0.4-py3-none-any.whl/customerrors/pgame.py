import pygame
import sys
import os

pygame.init()

screen = pygame.display.set_mode([720, 720])
pygame.display.set_caption("Test Game")

while True:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
