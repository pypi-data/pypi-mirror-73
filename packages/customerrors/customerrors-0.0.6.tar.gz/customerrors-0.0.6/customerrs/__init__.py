import pygame
import sys
import os

def draw():
    global yes
    pygame.init()
    screen = pygame.display.set_mode([1000,1000])
    pygame.display.set_caption("File.pyc")

    screen.fill((0,100,200))
    cat = pygame.image.load(os.path.join('customerrs\images', 'test.png'), "Cat")
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

class CustomError(Exception):
    """Base class for exceptions in this module."""
    pass

class InputCustomError(CustomError):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TransitionCustomError(CustomError):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, nextt, message):
        self.previous = previous
        self.next = nextt
        self.message = message

class ErrorTest(CustomError):
    def __init__(self, error, message):
        self.expression = error
        self.message = message



if __name__ == "__main__":
    draw()
