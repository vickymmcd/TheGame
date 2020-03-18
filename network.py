import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.game, self.player_num = self.connect()

    def get_game(self):
        # The state is the entire game object
        return self.game

    def get_player_num(self):
        return self.player_num

    def connect(self):
        try:
            print("hiya friend")
            self.client.connect(self.addr)
            game, player_num = pickle.loads(self.client.recv(2048))
            return game, player_num
        except:
            pass

    def send(self, data):
        try:
            # Send the current game object
            self.client.send(pickle.dumps(data))
            data = pickle.loads(self.client.recv(2048))
            game, _ = data
            return game
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            game, _ = pickle.loads(self.client.recv(2048))
            return game
        except socket.error as e:
            print(e)
