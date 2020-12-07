from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin, login_required
from wtforms.validators import DataRequired
from datetime import datetime
import socket
from game import Game
from player import Player
from deck import Deck
from _thread import start_new_thread
from thegame import theGame
from secret import SECRET_KEY


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class UserPlays():
    def __init__(self):
        self.plays = {}

    def add_user(self, player_id):
        self.plays[player_id] = None

    def set_play(self, player_id, pile_idx, card_idx):
        self.plays[player_id] = (pile_idx, card_idx)

    def get_play(self, player_id):
        return self.plays[player_id]

    def complete_play(self, player_id):
        self.plays[player_id] = None

class GameUser(UserMixin):
    def __init__(self, username):
        self.username = username
        self.pile_idx = None

    def get_id(self):
        return self.username

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username

users = []
num_players = 0
user_dict = {}
user_plays = UserPlays()
# Initiate the game object
game = Game()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return GameUser(user_id)
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    global num_players
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = GameUser(form.username.data)
        login_user(user)
        print(user)
        users.append(user)
        user_plays.add_user(num_players)
        num_players += 1
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/')
@login_required
def sessions():
    return render_template('session.html')


@app.route('/index')
@login_required
def index():
    print(users)
    print(num_players)
    return render_template('session.html')

@app.route('/logout')
def logout():
    global game
    global num_players
    logout_user()
    # someone logging out resets the game state
    users = []
    num_players = 0
    user_dict = {}
    user_plays = UserPlays()
    game = Game()
    return redirect(url_for('login'))


@app.route('/user')
@login_required
def user():
    print(current_user)
    user = current_user
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@socketio.on('joined')
def handle_user_joined_event(json, methods=['GET', 'POST']):
    global game
    print("GAME", game)
    print('received my event: ' + str(json))
    print(request.sid)

    if len(user_dict.keys()) >= 1:
        already_here_json = {"user_name": "computer", "message": "These users: " + str(list(user_dict.keys())) + " are already here!"}
        socketio.emit('my response', already_here_json, room=request.sid)
    user_dict[json["user_name"]] = request.sid
    joined_json = {"user_name": "computer", "message": json["user_name"] + " has joined!"}
    socketio.emit('my response', joined_json)
    print(users)
    print(current_user)
    start_new_thread(theGame, (game, users.index(current_user), request.sid, socketio, user_plays))

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    print(users)
    if "my_list" in json:
        print(json["my_list"])
    if "message" in json:
        if json["message"] == "ready":
            json["message"] = "Starting game with " + str(num_players) + " players!"
            game.deal_cards(num_players)
    socketio.emit('my response', json)

@socketio.on('pile_idx')
def update_pile_idx(json, methods=['GET', 'POST']):
    print("updating user plays")
    current_user.pile_idx = json["pile_idx"]

@socketio.on('card_idx')
def update_card_idx(json, methods=['GET', 'POST']):
    user_plays.set_play(users.index(current_user), current_user.pile_idx, json["card_idx"])

@socketio.on('GameObject')
def receive_game_object(json, methods=['GET', 'POST']):
    print("before " + game.to_json())
    game.deck = Deck(json["deck"])
    game.piles = json["piles"]
    players = []
    player_json = json["players"]
    for player in player_json:
        players.append(Player(num_players, game.deck, player["player_id"], player["hand_size"], player["hand"]))
    game.players = players
    game.curr_turn = json["curr_turn"]
    game.gameover = json["gameover"]
    print("after " + game.to_json())


if __name__ == '__main__':
    socketio.run(app, debug=True)
