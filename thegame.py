import pygame
from game import Game
from network import Network

network = Network()
game = network.get_game()
player_number = network.get_player_num()
gameover = False
while not gameover:
    print(game.curr_turn)
    if game.curr_turn == player_number:

        gameover = game.take_turn(game.players[player_number])
        if gameover:
            break
        game.players[player_number].end_turn()

        game.curr_turn = (game.curr_turn + 1) % game.num_players

        game = network.send(game)

    game = network.receive()
    if len(game.deck.get_deck_list()) == 0:
        print("Congrats! Yall beat The Game!!")
        gameover = True

print("GG")
