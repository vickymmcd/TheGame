import socket
from _thread import *
import sys
from game import Game
from player import Player
import pickle
import os

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
    '''
    packet = pickle.dumps((game, currentPlayer))
    length = struct.pack('!I', len(packet))
    packet = length + packet
    conn.send(packet)
    reply = ""
    while True:
        try:
            # Get the new game data
            buf = b''
            while len(buf) < 4:
                buf += conn.recv(4 - len(buf))

            length = struct.unpack('!I', buf)[0]
            message = b''
            while len(message) < length:
                message += conn.recv()
            data = pickle.loads(message)
            game, _ = data
    '''
    conn.send(pickle.dumps((game, currentPlayer)))
    reply = ""
    while True:
        try:
            # Get the new game data
            data = pickle.loads(conn.recv(4000))
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

    conn.close()
    print(f"Player {currentPlayer} has lost connection. Restart server.")
    os._exit(0)

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
