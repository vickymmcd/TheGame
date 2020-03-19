import pygame
from pygame.locals import *

from game import Game
from network import Network
from sys import exit
 
class App:

    

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.clock = None
        self.font = None
        self.windowWidth = 1500
        self.windowHeight = 875
        self.x = 10
        self.y = 10
        self.network = None
        self.game = None
        self.player_number = None
        
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        self._running = True
        #setting the caption 
        pygame.display.set_caption('The Game')
        #setting the Clock
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 50)
        #self._image_surf = pygame.image.load("pygame.png").convert()
        self.network = Network()
        self.game = self.network.get_game()
        self.player_number = self.network.get_player_num()
        return True
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            x, y = event.pos
            print(x,y)
            '''
            for card in game.player[self.player_number-1].hand:
                if card.get_rect().collidepoint(x, y):
                    print("collide!")'''
    
    def on_loop(self):
        pass
    
    def on_render(self):
        x0 = 150
        y0 = 600
        #self._display_surf.blit(self._image_surf,(self.x,self.y))
        for card in self.game.players[self.player_number-1].hand:
            #print(card.card_img)
            print("wooo")
            card_img = 'assets/cards/Asset ' + str(card.card_val) + '.png'
            sprite_img = pygame.image.load(card_img).convert_alpha()
            sprite_img = pygame.transform.scale(sprite_img, (150, 220))
            self._display_surf.blit(sprite_img, (x0, y0))
            #card.rect = Rect(x0, y0, 150, 220)
            x0 += 175
        pygame.display.flip()
 
    def on_cleanup(self):
        print("Game ended with " + str(len(self.game.deck.get_deck_list())) + " cards left in the deck")

        if len(self.game.deck.get_deck_list()) > 0:
            print("Game over, yall lost.")
        elif len(self.game.deck.get_deck_list()) == 0:
            print("Congrats! Yall beat The Game!!")
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        print("Welcome! You are player " + str(self.player_number))
        while( self._running ):
            for event in pygame.event.get():
                print("event wooo")
                if self.game.curr_turn == self.player_number:
                    self.game.gameover = self.on_event(event)
                    self.game.gameover = self.game.take_turn(self.game.players[self.player_number])
                    if self.game.gameover:
                        self.game = self.network.send((self.game, self.player_number))
                        break
                    self.game.players[self.player_number].end_turn()

                    self.game.curr_turn = (self.game.curr_turn + 1) % self.game.num_players

                    self.game = self.network.send((self.game, self.player_number))

                else:
                    if self.game.curr_turn == -1:
                        print("Waiting for more players to join..")
                        print("If you would like to start indicate this on the server!")
                    else:
                        print("Wait for player " + str(self.game.curr_turn) + " to take their turn!")
                    self.game = self.network.receive()

                if len(self.game.deck.get_deck_list()) == 0:
                    self.game.gameover = True
                    self.game = self.network.send((self.game, self.player_number))
                    self._running = False
            self.on_loop()
            self.on_render()
        self.on_cleanup()
        
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()