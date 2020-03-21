import pygame
from pygame.locals import *

from game import Game
from network import Network
from buttons import EndTurnButton, PlayCardButton
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
        self.endTurnButton = None
        self.playCardButton = None
        self.selected_card_id = None
        self.selected_pile_id = None
        self.moves_made = 0
        
 
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
        self.endTurnButton = EndTurnButton(self._display_surf)
        self.playCardButton = PlayCardButton(self._display_surf)
        return True

    def card_select(self, x, y):
        for idx, card in enumerate(self.game.players[self.player_number-1].hand):
            if card.rect.collidepoint(x, y):
                if self.selected_card_id == idx:
                    self.selected_card_id = None
                else:
                    self.selected_card_id = idx

                print("Selected card id: " + str(self.selected_card_id))
                return False
        return False
    
    def pile_select(self, x,y):
        for idy, pile in enumerate(self.game.piles):
            if pile.rect.collidepoint(x,y):
                if self.selected_pile_id == idy:
                    self.selected_pile_id = None
                else:
                    self.selected_pile_id = idy
                print("Selected pile id: " + str(self.selected_pile_id))
                return False
        return False

    def end_turn(self):
        if self.game.gameover:
            self.game = self.network.send((self.game, self.player_number))
            return True
        self.game.players[self.player_number].end_turn()
        self.game.curr_turn = (self.game.curr_turn + 1) % self.game.num_players
        self.game = self.network.send((self.game, self.player_number))
        self.moves_made = 0
        return False

    def button_select(self,x,y):
        if self.endTurnButton.rect.collidepoint(x, y):
            if (self.game.deck.get_deck_size() == 0 and self.moves_made >= 1) or self.moves_made >= 2:
                return self.end_turn()
            else:
                print("You need to play more cards!")

        if self.playCardButton.rect.collidepoint(x,y):
            if self.selected_card_id != None and self.selected_pile_id != None:
                play_sucess = self.game.take_turn(self.game.players[self.player_number-1], self.selected_pile_id, self.selected_card_id)
                if play_sucess:
                    self.moves_made +=1
                    self._display_surf.fill((0,0,0))
            else:
                print("select a card and a pile")
        return False

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            if not self.game.possible_moves(self.game.players[self.player_number-1]):
                if self.game.deck.get_deck_size() > 0:
                    if self.moves_made < 2:
                        self.game.gameover = True
                elif self.moves_made == 0:
                    self.game.gameover = True
                print("No more possible moves, ending turn")
                self.end_turn()
                
            # Set the x, y postions of the mouse click
            x, y = event.pos
            return_val = False
            if y < 110:
                return_val = self.button_select(x,y)
            elif y >= 110 and y <=550:
                return_val = self.pile_select(x,y)
            else:
                return_val = self.card_select(x,y)
            self.on_render()
            return return_val
            

    def on_loop(self):
        pass

    def display_hand(self):
        x0 = 150
        y0 = 600

        for card in self.game.players[self.player_number-1].hand:
            card_img = 'assets/cards/Asset ' + str(card.card_val) + '.png'
            sprite_img = pygame.image.load(card_img).convert_alpha()
            sprite_img = pygame.transform.scale(sprite_img, (150, 220))
            self._display_surf.blit(sprite_img, (x0, y0))
            card.create_rect(x0, y0, 150, 220)
            x0 += 175

    def display_piles(self):
        x0 = 600
        y0 = 75
        rotating_id = 0
        for pile in self.game.piles:
            card_img = 'assets/cards/Asset ' + str(pile) + '.png'
            sprite_img = pygame.image.load(card_img).convert_alpha()
            sprite_img = pygame.transform.scale(sprite_img, (150, 220))
            self._display_surf.blit(sprite_img, (x0, y0))
            pile.create_rect(x0, y0, 150, 220)
            if rotating_id == 0:
                x0 += 175
                rotating_id += 1
            elif rotating_id == 1:
                y0 += 250
                rotating_id += 1
            elif rotating_id == 2:
                x0 -= 175
                rotating_id += 1
    
    def on_render(self):
        self.endTurnButton = EndTurnButton(self._display_surf)
        self.playCardButton = PlayCardButton(self._display_surf)
        self.display_hand()
        
        self.display_piles()
        #self._display_surf.fill((0,0,0))
        pygame.display.update()
 
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
                if self.game.curr_turn == self.player_number:
                    #self.game.gameover = 
                    self.on_event(event)
                    '''
                    self.game.gameover = self.game.take_turn(self.game.players[self.player_number])
                    if self.game.gameover:
                        self.game = self.network.send((self.game, self.player_number))
                        break
                    self.game.players[self.player_number].end_turn()

                    self.game.curr_turn = (self.game.curr_turn + 1) % self.game.num_players

                    self.game = self.network.send((self.game, self.player_number))
                    '''

                else:
                    if self.game.curr_turn == -1:
                        print("Waiting for more players to join..")
                        print("If you would like to start indicate this on the server!")
                    else:
                        print("Wait for player " + str(self.game.curr_turn) + " to take their turn!")
                        self.on_render()
                        self.game.players[self.player_number-1].print_hand()
                    self.game = self.network.receive()
                #self.game.players[self.player_number-1].print_hand()
                if len(self.game.deck.get_deck_list()) == 0:
                    self.game.gameover = True
                    self.game = self.network.send((self.game, self.player_number))
                    self._running = False
                
            self.on_render()
        self.on_cleanup()
        
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()