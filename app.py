from boggle import Boggle
from flask import Flask, render_template, request, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.debug = True
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


def make_board():
    """ Make a Boggle game board from the boggle_game instance of the Boggle class """
    boggle_board = boggle_game.make_board()
    session['board'] = boggle_board
    return boggle_board

def check_word(word, board):
    """ Check if a word is a valid word and on the board """
    isWord = word in boggle_game.words
    check_valid = boggle_game.check_valid_word(board, word)

    if isWord and check_valid == "ok":
        code = "ok"
    elif isWord and check_valid == "not-on-board":
        code = "not-on-board"
    else: 
        code = "not-word"
    return code

def add_game_played():
    """ Add one to the number of games played """
    session['games_played'] = session.get('games_played', 0) + 1

def check_high_score(score): 
    """ Check if there is a new high score """   
    session['high_score'] = max(session.get('high_score', 0), score)


@app.route('/')
def show_start():
    """ Make the Boggle board and show the start buttone """   

    boggle_board = make_board()
    return render_template('index.html', board = boggle_board)

@app.route('/guess')
def make_guess():
    """ Check if a user's guess is valid and on the board """   

    guess = request.args["guess"]
    code = check_word(guess, session['board'])
    return jsonify({"result": code})

@app.route('/end', methods=["POST"])
def end_game():
    """ Increment games played and check for a new high score at the end of a game """   

    add_game_played()

    score = request.json['score']
    check_high_score(score)

    return jsonify({"games_played": session['games_played'], "high_score": session['high_score']})

