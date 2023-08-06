import pygame
import sys
import os
from main.customerrors import ErrorTest

yes = True

def draw():
    global yes
    pygame.init()
    screen = pygame.display.set_mode([1000,1000])
    pygame.display.set_caption("File.pyc")

    screen.fill((0,100,200))
    cat = pygame.image.load(os.path.join('main\images', 'test.png'), "Cat")
    pygame.display.flip()
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                raise ErrorTest("?", "!")
                sys.exit()
            if evt.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if x >= 400 and y >= 400:
                    pygame.image.save(screen, os.path.join('images', 'screenshot.png'))
                
            if evt.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                screen.blit(cat, (x, y))
                #raise TypeError("Cat is a cat")
        pygame.display.flip()

if __name__ == "__main__":
    draw()
