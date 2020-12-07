from game import Game
from network import Network

def theGame(game, player_num, user_room_code, socketio, user_plays):
    print("GAME", game)
    network = Network(game, player_num, user_room_code, socketio)
    game = network.get_game()
    player_number = network.get_player_num()
    #print("Welcome! You are player " + str(player_number))
    while not game.gameover:
        print(game.curr_turn)
        if game.curr_turn == player_number:

            socketio.emit('get_next_move', {}, room=user_room_code)
            while user_plays.get_play(player_num) is None:
                pass
            print("in a miracle, i got the updated play")
            pile_idx, card_idx = user_plays.get_play(player_num)
            game.gameover = game.take_turn(game.players[player_number], pile_idx, card_idx)
            if game.gameover:
                network.send((game, player_number))
                break
            game.players[player_number].end_turn()

            game.curr_turn = (game.curr_turn + 1) % game.num_players

            network.send((game, player_number))

        else:
            if game.curr_turn == -1:
                network.display_message("waiting for more players to join..")
                network.display_message("if you would like to start now, type 'ready'")
                while game.curr_turn == -1:
                    # wait until the game starts!
                    pass
            else:
                network.display_message("wait for player " + users[game.curr_turn] + " to take their turn!")
            #game = network.receive()

        if len(game.deck.get_deck_list()) == 0:
            game.gameover = True
            network.send((game, player_number))

    network.display_message("Game ended with " + str(len(game.deck.get_deck_list())) + " cards left in the deck")

    if len(game.deck.get_deck_list()) > 0:
        network.display_message("Game over, yall lost.")
    elif len(game.deck.get_deck_list()) == 0:
        network.display_message("Congrats! Yall beat The Game!!")
