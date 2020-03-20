import pygame
from pygame.locals import *

# end turn button
class EndTurnButton:
    def __init__(self, gameDisplay):
        self.red = (200,0,0)
        self.green = (0,200,0)
        self.blue = (0, 0, 200)

        self.bright_red = (255,0,0)
        self.bright_green = (0,255,0)
        pygame.draw.rect(gameDisplay, self.blue,(75,50,150,50))

# confirm card play button
class PlayCardButton:
    def __init__(self, gameDisplay):
        self.red = (200,0,0)
        self.green = (0,200,0)
        self.blue = (0, 0, 200)

        self.bright_red = (255,0,0)
        self.bright_green = (0,255,0)
        pygame.draw.rect(gameDisplay, self.green,(1300, 50,150,50))

