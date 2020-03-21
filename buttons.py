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
        self.rect = Rect(75,50,150,50)
        font = pygame.font.Font('freesansbold.ttf', 32) 
        text = font.render('End turn', True, self.green, self.blue) 
  
        # create a rectangular object for the 
        # text surface object 
        textRect = text.get_rect()  
        
        # set the center of the rectangular object. 
        textRect.center = (150, 75) 

        gameDisplay.blit(text, textRect) 

# confirm card play button
class PlayCardButton:
    def __init__(self, gameDisplay):
        self.red = (200,0,0)
        self.green = (0,200,0)
        self.blue = (0, 0, 200)

        self.bright_red = (255,0,0)
        self.bright_green = (0,255,0)
        pygame.draw.rect(gameDisplay, self.green,(1300, 50,150,50))
        self.rect = Rect(1300, 50,150,50)
        font = pygame.font.Font('freesansbold.ttf', 32) 
        text = font.render('Play card', True, self.blue, self.green) 
  
        # create a rectangular object for the 
        # text surface object 
        textRect = text.get_rect()  
        
        # set the center of the rectangular object. 
        textRect.center = (1375, 75) 

        gameDisplay.blit(text, textRect) 

