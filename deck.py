from random import randint

class Deck:
    def __init__(self):
        # create the deck of cards from 2-99
        self.deck = []
        for i in range(2, 48):
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

# represent a playing card in The Game
class PlayingCard:
    def __init__(self, value):
        self.card_val = value
        self.card_img = 'woooo' #'assets/cards/' + str(self.card_val) + '.png'

    def __str__(self):
        return str(self.card_val)
