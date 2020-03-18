import socket
from _thread import *
import sys
from game import Game
from player import Player
import pickle

# If this doens't work: Use ipconfig, then paste your IPV4 address here
server = socket.gethostbyname(socket.gethostname())

port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print("Waiting for a connection, Server Started")

# Initiate the game object
game = Game()

def threaded_client(conn, currentPlayer):
    global game
    conn.send(pickle.dumps((game, currentPlayer)))
    reply = ""
    while True:
        try:
            # Get the new game data
            data = pickle.loads(conn.recv(2048))
            game, _ = data

            if not data:
                print("Disconnected")
                break
            else:
                # Send back the updated game data
                reply = data
                print("Received: ", data)
                print("Sending : ", reply)

            broadcast(reply)
        except:
            break

    print("Lost connection")
    conn.close()

def broadcast(game_state):
    for conn in client_conns:
        conn.sendall(pickle.dumps(game_state))


num_players = 0
client_conns = []
while True:
    conn, addr = s.accept()
    client_conns.append(conn)
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, num_players))
    num_players += 1
    keep_waiting = input("Wait for more players? (y/n) ")
    if keep_waiting == "n":
        break

game.deal_cards(num_players)
for conn in client_conns:
    conn.sendall(pickle.dumps((game, -1)))
while True:
    pass