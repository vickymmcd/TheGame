from random import randint
import pygame

# represent a playing card in The Game
class PlayingCard:
    def __init__(self, value):
        self.card = value

    def __str__(self):
        return str(self.card)

class Deck:
    def __init__(self):
        # create the deck of cards from 2-99
        self.deck = []
        for i in range(2, 100):
            self.deck.append(PlayingCard(i))

    def get_deck_list(self):
        return self.deck

    # draw a single card from the deck
    def draw_card(self):
        rand_card = randint(0, len(self.deck)-1)
        return self.deck.pop(rand_card)

    # draws a hand with num cards
    def draw_hand(self, num):
        hand = []
        for i in range(0, num):
            hand.append(self.draw_card())
        return hand

    def __str__(self):
        deck_str = ""
        for i in range(0, len(self.deck)-1):
            deck_str = deck_str + str(self.deck[i]) + ", "
        deck_str = deck_str + str(self.deck[i+1])
        return deck_str

class InvalidNumberOfPlayersException(Exception):
    pass

class Player:
    def __init__(self, num_players, deck):
        self.num_players = num_players
        self.deck = deck
        if num_players >= 3 and num_players <= 5:
            self.hand_size = 6
            self.hand = deck.draw_hand(6)
        elif num_players == 2:
            self.hand_size = 7
            self.hand = deck.draw_hand(7)
        elif num_players == 1:
            self.hand_size = 8
            self.hand = deck.draw_hand(8)
        else:
            raise InvalidNumberOfPlayersException

    # peeks card in hand at index idx before playing it need to see if valid!
    def peek_card(self, idx):
        return self.hand[idx]

    # plays card in their hand at index idx
    def play_card(self, idx):
        return self.hand.pop(idx)

    def end_turn(self):
        while len(self.hand) < self.hand_size:
            self.hand.append(deck.draw_card())

    def print_hand(self):
        hand_str = ""
        for i in range(0, len(self.hand)-1):
            hand_str = hand_str + str(self.hand[i]) + ", "
        hand_str = hand_str + str(self.hand[i+1])
        print(hand_str)
        return hand_str

class Game:
    # piles 1 and 2 ascending, piles 3 & 4 descending
    def __init__(self, num_players):
        self.num_players = num_players
        self.deck = Deck()
        self.piles = [1, 1, 100, 100]
        self.players = []
        for i in range(0, self.num_players):
            self.players.append(Player(self.num_players, self.deck))

    def print_piles(self):
        print("Ascending: " + str(self.piles[0]) + ", " + str(self.piles[1]))
        print("Descending: " + str(self.piles[2]) + ", " + str(self.piles[3]))

    def take_turn(self, player):
        keep_playing = "y"
        cards_played = 0
        while keep_playing == "y":
            # check whether game is over
            if not self.possible_moves(player):
                if cards_played < 2:
                    print("Game over, yall lost.")
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
                cards_played += 1
            if cards_played >= 2:
                keep_playing = input("Would you like to play another card (y/n)? ")

    def possible_moves(self, player):
        # check to see if there are any possible moves for that player
        for pile_idx in range(0, 4):
            for card_idx in range(0, len(player.hand)):
                if check_play_validity(player, pile_idx, card_idx):
                    return True
        return False

    def check_play_validity(self, player, pile_idx, card_idx):
        pile = self.piles[pile_idx]
        card = player.peek_card(card_idx).card
        if pile_idx == 0 or pile_idx == 1:
            if card > pile or card == pile - 10:
                player.play_card(card_idx)
                self.piles[pile_idx] = card
                return True
            else:
                print("invalid play")
                return False
        elif pile_idx == 2 or pile_idx == 3:
            if card < pile or card == pile + 10:
                player.play_card(card_idx)
                self.piles[pile_idx] = card
                return True
            else:
                print("invalid play")
                return False
        return False

    def run_gameplay(self):
        for player in self.players:
            self.take_turn(player)
        if len(self.deck.get_deck_list()) == 0:
            print("Congrats! Yall beat The Game!!")

game = Game(2)
game.run_gameplay()
