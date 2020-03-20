import pygame
from pygame.locals import *

# represent a playing card in The Game
class PlayingCard:
    def __init__(self, value):
        #self.stringiii = "what the hell"
        self.card_val = value
        
        self.rect = None
        #self.card_img = 'assets/cards/Asset ' + str(value) + '.png'

    def create_rect(self, left, top, width, height):
        self.rect = Rect(left, top, width, height)

    def __str__(self):
        return str(self.card_val)
