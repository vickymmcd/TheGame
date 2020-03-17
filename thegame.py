import pygame
from game import Game
from network import Network

class InvalidNumberOfPlayersException(Exception):
    pass

game = Game(2)
game.run_gameplay()
