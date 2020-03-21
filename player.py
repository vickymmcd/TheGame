class Player:
    def __init__(self, num_players, deck, player_id):
        self.num_players = num_players
        self.deck = deck
        self.player_id = player_id
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
        self.hand.sort(key=lambda x: x.card_val)

    # peeks card in hand at index idx before playing it need to see if valid!
    def peek_card(self, idx):
        return self.hand[idx]

    # plays card in their hand at index idx
    def play_card(self, idx):
        return self.hand.pop(idx)

    def end_turn(self):
        while len(self.hand) < self.hand_size and len(self.deck.get_deck_list()) > 0:
            print("drawing new card")
            self.hand.append(self.deck.draw_card())
        self.hand.sort(key=lambda x: x.card_val)

    def print_hand(self):
        hand_str = ""
        for i in range(0, len(self.hand)-1):
            hand_str = hand_str + str(self.hand[i]) + ", "
        hand_str = hand_str + str(self.hand[i+1])
        print(hand_str)
        return hand_str


class InvalidNumberOfPlayersException(Exception):
    pass
