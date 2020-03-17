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

s.listen(5)
print("Waiting for a connection, Server Started")

# Initiate the game object
game = Game(5)

def threaded_client(conn):
    conn.send(pickle.dumps(game))
    reply = ""
    while True:
        try:
            # Get the new game data
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break
            else:
                # Send back the updated game data
                reply = data
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
