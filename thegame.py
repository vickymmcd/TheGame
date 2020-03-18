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

#Main loop:
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            #exit command
            exit()
    gameover = False
    while not gameover:
        print(game.curr_turn)
        print(game.players)
        if game.curr_turn == player_number:
            screen = game.players[player_number-1].display_hand(screen)
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
        pygame.display.update()
        #Limiting the fps to 10
        time_passed = clock.tick(10)

print("GG")
