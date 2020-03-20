import pygame
from pygame.locals import *

# represent a playing card in The Game
class PlayingCard:
    def __init__(self, value):
        self.card_val = value
        
        self.rect = None

    def create_rect(self, left, top, width, height):
        self.rect = Rect(left, top, width, height)

    def __str__(self):
        return str(self.card_val)
