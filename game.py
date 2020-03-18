from player import Player
from network import Network
from deck import Deck

class Game:
    # piles 1 and 2 ascending, piles 3 & 4 descending
    def __init__(self):
        self.deck = Deck()
        self.piles = [1, 1, 100, 100]
        self.players = []
        self.curr_turn = -1

    def deal_cards(self, num_players):
        self.num_players = num_players
        for i in range(0, self.num_players):
            self.players.append(Player(self.num_players, self.deck, i))
        self.curr_turn = 0

    def print_piles(self):
        print("Ascending: " + str(self.piles[0]) + ", " + str(self.piles[1]))
        print("Descending: " + str(self.piles[2]) + ", " + str(self.piles[3]))

    # returns true if this player's turn ends the game, false otherwise
    def take_turn(self, player):
        keep_playing = "y"
        cards_played = 0
        while keep_playing == "y":
            # check whether game is over
            if not self.possible_moves(player):
                if cards_played < 2:
                    print("Game over, yall lost.")
                    print("Game ended with " + str(len(self.deck.get_deck_list())) +
                        " cards left in the deck.")
                    return True
                    break
                print("No more possible moves, ending turn")
                break
            print("PLAYER HAND")
            player.print_hand()
            print("CURRENT PILES")
            self.print_piles()
            card_idx = int(input("What card would you like to play? "))
            pile_idx = int(input("What pile would you like to place it on? "))
            if self.check_play_validity(player, pile_idx, card_idx):
                card = player.play_card(card_idx).card_val
                self.piles[pile_idx] = card
                cards_played += 1
            else:
                print("INVALID PLAY!")
            if cards_played >= 2:
                keep_playing = input("Would you like to play another card (y/n)? ")

        return False

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
            if card1 > pile or card1 == pile - 10:
                return True
            else:
                return False
        elif pile_idx == 2 or pile_idx == 3:
            if card1 < pile or card1 == pile + 10:
                return True
            else:
                return False
        return False

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
