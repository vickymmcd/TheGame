from random import randint
from playingcard import PlayingCard

class Deck:
    def __init__(self):
        # create the deck of cards from 2-99
        self.deck = []

    def on_init(self):
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

    def get_deck_size(self):
        return len(self.deck)

    def __str__(self):
        deck_str = ""
        for i in range(0, len(self.deck)-1):
            deck_str = deck_str + str(self.deck[i]) + ", "
        deck_str = deck_str + str(self.deck[i+1])
        return deck_str

