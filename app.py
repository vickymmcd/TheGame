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
        self.card_rect = None
        self.pile_rect = None
        self.notification_rect = None
        self.num_cards_rect = None


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
        player_deck = self.game.players[self.player_number].hand
        for idx, card in enumerate(player_deck):
            if card.rect.collidepoint(x, y):
                if self.selected_card_id == idx:
                    self.selected_card_id = None
                else:
                    self.selected_card_id = idx

                if(self.selected_card_id != None):
                    display_info = f"Selected card: {player_deck[self.selected_card_id]}"
                    print(display_info)
                    card_rect = self.display_text(display_info, 10, self.windowHeight//3 - 25, self.card_rect)
                    self.card_rect = card_rect
                    return False
        return False

    def display_text(self, display_info, width, height, prev_rect):
        # Gives on-screen feedback to the user
        screen = pygame.display.get_surface()
        if(prev_rect != None):
            screen.fill(pygame.Color("black"), prev_rect)
        if(self.notification_rect != None):
            screen.fill(pygame.Color("black"), self.notification_rect)

        green = (0, 255, 0)
        blue = (0, 0, 128)
        text = self.font.render(display_info, True, pygame.Color("white"))
        textRect = text.get_rect()

        # set the center of the rectangular object.
        textRect.topleft = (width, height)
        self.textRect = textRect
        self._display_surf.blit(text, textRect)
        return textRect

    def pile_select(self, x,y):
        for idy, pile in enumerate(self.game.piles):
            if pile.rect.collidepoint(x,y):
                if self.selected_pile_id == idy:
                    self.selected_pile_id = None
                else:
                    self.selected_pile_id = idy

                if(self.selected_pile_id != None):
                    display_info = f"Selected pile: {self.game.piles[self.selected_pile_id]}"
                    print(display_info)
                    pile_rect = self.display_text(display_info, 10, self.windowHeight//3 + 25, self.pile_rect)
                    self.pile_rect = pile_rect
                    return False
        return False

    def end_turn(self):
        if self.game.gameover:
            self.game = self.network.send((self.game, self.player_number))
            return True
        self.game.players[self.player_number].end_turn()
        self.on_render()
        self.game.curr_turn = (self.game.curr_turn + 1) % self.game.num_players
        self.game = self.network.send((self.game, self.player_number))
        self.moves_made = 0

        cards_in_deck = len(self.game.deck.get_deck_list())
        display_info = f"Cards left in deck: {cards_in_deck}"
        num_cards_rect = self.display_text(display_info, 2*self.windowWidth//3, self.windowHeight//3, self.num_cards_rect)
        self.num_cards_rect = num_cards_rect
        return False

    def button_select(self,x,y):
        display_info = ""

        if self.endTurnButton.rect.collidepoint(x, y):
            if (self.game.deck.get_deck_size() == 0 and self.moves_made >= 1) or self.moves_made >= 2:
                return self.end_turn()
            else:
                display_info = "You need to play more cards!"
                print(display_info)

        if self.playCardButton.rect.collidepoint(x,y):
            if self.selected_card_id != None and self.selected_pile_id != None:
                play_sucess = self.game.take_turn(self.game.players[self.player_number], self.selected_pile_id, self.selected_card_id)
                if play_sucess:
                    self.moves_made +=1
                    self._display_surf.fill((0,0,0))
            else:
                display_info = "Select a card and a pile"
                print(display_info)

        if(display_info != ""):
            notification_rect = self.display_text(display_info, self.windowWidth//3 + 25, 10, self.notification_rect)
            self.notification_rect = notification_rect
        return False

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            if not self.game.possible_moves(self.game.players[self.player_number]):
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

        for card in self.game.players[self.player_number].hand:
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
        print("and with " + str(self.game.get_num_cards_in_hands()) + " cards left in players' hands")

        if len(self.game.deck.get_deck_list()) > 0:
            print("Game over, yall lost.")
        elif len(self.game.deck.get_deck_list()) == 0 and self.game.get_num_cards_in_hands() == 0:
            print("Congrats! Yall beat The Game!!")
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        display_info = f"Welcome! You are player {self.player_number}"
        notification_rect = self.display_text(display_info, self.windowWidth//3 + 25, 10, self.notification_rect)
        self.notification_rect = notification_rect
        print(display_info)

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
                        display_info = f"Waiting for player {self.game.curr_turn} to take their turn!"
                        notification_rect = self.display_text(display_info, self.windowWidth//3 + 25, 10, self.notification_rect)
                        self.notification_rect = notification_rect

                        print(display_info)
                        self.on_render()
                        self.game.players[self.player_number].print_hand()
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
