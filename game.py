from player import Player
from network import Network
from deck import Deck
from playingcard import PlayingCard

class Game:
    # piles 1 and 2 ascending, piles 3 & 4 descending
    def __init__(self):
        self.deck = Deck()
        self.piles = []
        self.players = []
        self.curr_turn = -1
        self.gameover = False

    def deal_cards(self, num_players):
        self.deck.on_init()
        self.piles = [PlayingCard(1), PlayingCard(1), PlayingCard(100), PlayingCard(100)]
        self.num_players = num_players
        for i in range(0, self.num_players):
            self.players.append(Player(self.num_players, self.deck, i))
        self.curr_turn = 0

    def print_piles(self):
        print("Ascending: " + str(self.piles[0].card_val) + ", " + str(self.piles[1].card_val))
        print("Descending: " + str(self.piles[2].card_val) + ", " + str(self.piles[3].card_val))

    # returns true if this player's turn ends the game, false otherwise
    def take_turn(self, player, pile_idx, card_idx):
        '''
        keep_playing = "y"
        cards_played = 0
        while keep_playing == "y":
            # check whether game is over

            print("PLAYER HAND")
            player.print_hand()
            print("CURRENT PILES")
            self.print_piles()
            card_idx = int(input("What card would you like to play? "))
            pile_idx = int(input("What pile would you like to place it on? "))
            '''
        if self.check_play_validity(player, pile_idx, card_idx):
            card = player.play_card(card_idx)
            self.piles[pile_idx] = card
            return True
        else:
            print("INVALID PLAY!")
            return False
            '''
            if cards_played >= 2:
                keep_playing = input("Would you like to play another card (y/n)? ")
            '''


    def possible_moves(self, player):
        # check to see if there are any possible moves for that player
        for pile_idx in range(0, 4):
            for card_idx in range(0, len(player.hand)):
                if self.check_play_validity(player, pile_idx, card_idx):
                    return True
        return False

    def check_play_validity(self, player, pile_idx, card_idx):
        pile = self.piles[pile_idx]
        card1 = player.peek_card(card_idx).card_val
        if pile_idx == 0 or pile_idx == 1:
            if card1 > pile.card_val or card1 == pile.card_val - 10:
                return True
            else:
                return False
        elif pile_idx == 2 or pile_idx == 3:
            if card1 < pile.card_val or card1 == pile.card_val + 10:
                return True
            else:
                return False
        return False

    def get_num_cards_in_hands(self):
        total = 0
        for player in self.players:
            total += len(player.hand)
        return total

    def run_gameplay(self):
        gameover = False
        # # Get the state of the game from the server
        # game_state = self.network.getState()

        while not gameover:
            for player in self.players:
                gameover = self.take_turn(player)
                if gameover:
                    break
                player.end_turn()

            if len(self.deck.get_deck_list()) == 0:
                print("Congrats! Yall beat The Game!!")
                gameover = True
