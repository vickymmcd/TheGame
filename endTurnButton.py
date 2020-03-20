import pygame
from pygame.locals import *

# represent a playing card in The Game
class EndTurnButton:
    def __init__(self, gameDisplay):
        self.red = (200,0,0)
        self.green = (0,200,0)

        self.bright_red = (255,0,0)
        self.bright_green = (0,255,0)
        pygame.draw.rect(gameDisplay, self.green,(150,450,100,50))

