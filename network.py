class Network:
    def __init__(self, game, player_num, user_room_code, socketio):
        self.game = game
        self.player_num = player_num
        self.user_room_code = user_room_code
        self.socketio = socketio

    def get_game(self):
        # The state is the entire game object
        print("GAME SELF", self.game)
        return self.game

    def get_player_num(self):
        return self.player_num

    def send(self, data):
        game_json = {"GameObject": self.game.to_json()}
        self.socketio.emit('game', game_json)

    def display_message(self, message):
        json = {"user_name": "computer", "message": message}
        self.socketio.emit('my response', json, room=self.user_room_code)

    # @self.socketio.on('game')
    # def receive(self, json, methods=['GET', 'POST']):
    #
