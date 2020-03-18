import pygame
from pygame.locals import*

from game import Game
from network import Network
from sys import exit

network = Network()
game = network.get_game()
player_number = network.get_player_num()

#starting the pygame     
pygame.init()
#creating the screen 400x400
screen = pygame.display.set_mode((1000, 700), 0, 32)
#setting the caption 
pygame.display.set_caption('The Game')
#setting the Clock
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 50)

print("Welcome! You are player " + str(player_number))
while not game.gameover:
    if game.curr_turn == player_number:

        game.gameover = game.take_turn(game.players[player_number])
        if game.gameover:
            game = network.send((game, player_number))
            break
        game.players[player_number].end_turn()

            game.curr_turn = (game.curr_turn + 1) % game.num_players

        game = network.send((game, player_number))

    else:
        if game.curr_turn == -1:
            print("Waiting for more players to join..")
            print("If you would like to start indicate this on the server!")
        else:
            print("Wait for player " + str(game.curr_turn) + " to take their turn!")
        game = network.receive()

    if len(game.deck.get_deck_list()) == 0:
        game.gameover = True
        game = network.send((game, player_number))

print("Game ended with " + str(len(game.deck.get_deck_list())) + " cards left in the deck")

if len(game.deck.get_deck_list()) > 0:
    print("Game over, yall lost.")
elif len(game.deck.get_deck_list()) == 0:
    print("Congrats! Yall beat The Game!!")
