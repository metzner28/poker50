from flask import Flask, flash, redirect, render_template, request, session
from helpers2 import Card, Hand, apology
from flask_session import Session
import random

app = Flask(__name__)

# homepage, player input
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return redirect("/hands")

# just shows the "about" html page
@app.route("/about")
def about():
    return render_template("about.html")

# hand inputs
@app.route("/hands")
def input_hands():
    players = request.args.get("players")
    try:
        players = int(players)
        if players < 2 or players > 10:
            return apology("between 2 and 10 players!")
        else:
            return render_template("hands.html", players=players)
    except:
        return apology("invalid players!")

# calculator!
@app.route("/calculate", methods=["POST"])
def calculate():
    values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
    suits = ['s','h','d','c']
    deck = [Card(value, suit) for value in values for suit in suits]
    hands = []

    # get hand inputs and actual number of players
    handinputs = request.form.getlist("hand")
    players = len(handinputs)

    if players == 0:
        return apology("forgot to input hands!")

    # store inputted hands in list, throw apology for invalid input
    for handinput in handinputs:
        try:
            card1 = Card(f"{handinput[0]}", f"{handinput[1]}")
            card2 = Card(f"{handinput[2]}", f"{handinput[3]}")
            hands.append((card1,card2))
            deck.remove(card1)
            deck.remove(card2)
        except (ValueError, IndexError):
            return apology("invalid cards!")

    # deal with board input if any, throw apology for invalid input
    boardinput = request.form.get("board")
    try:
        if len(boardinput) == 6:
            board1 = Card(f"{boardinput[0]}", f"{boardinput[1]}")
            board2 = Card(f"{boardinput[2]}", f"{boardinput[3]}")
            board3 = Card(f"{boardinput[4]}", f"{boardinput[5]}")
            deck.remove(board1)
            deck.remove(board2)
            deck.remove(board3)
        elif len(boardinput) == 8:
            board1 = Card(f"{boardinput[0]}", f"{boardinput[1]}")
            board2 = Card(f"{boardinput[2]}", f"{boardinput[3]}")
            board3 = Card(f"{boardinput[4]}", f"{boardinput[5]}")
            board4 = Card(f"{boardinput[6]}", f"{boardinput[7]}")
            deck.remove(board1)
            deck.remove(board2)
            deck.remove(board3)
            deck.remove(board4)
        else:
            if len(boardinput) != 0:
                return apology("invalid board!")
    except (ValueError, IndexError):
        return apology("invalid board!")

    # initialize counters and number of trials
    chop = 0
    TRIALS = 100000
    winners = [0 for p in range(players)]

    # run simulations
    for t in range(TRIALS):
        fullhands = []
        ranks = []

        # generate board
        if len(boardinput) == 6:
            board = [board1, board2, board3] + random.sample(deck,2)
        elif len(boardinput) == 8 and board4:
            board = [board1, board2, board3, board4] + random.sample(deck,1)
        else:
            board = random.sample(deck,5)

        # generate hands from board and rank each hand
        for h in hands:
            hand = Hand(h[0], h[1], board)
            fullhands.append(hand)
        for f in fullhands:
            rank = f.rank()
            ranks.append(rank)

        # make sure we have a rank for each hand, else crash
        assert len(ranks) == players

        # deal with ties and increment appropriate counter for winner, based on index
        if ranks.count(max(ranks)) != 1:
            chop += 1
        else:
            win = ranks.index(max(ranks))
            winners[win] += 1

    # generate probability percentages
    chop = round((chop/TRIALS)*100, 2)
    pcts = []
    for number in winners:
        pct = round((number / TRIALS) * 100, 2)
        pcts.append(pct)

    # put percentages in dict with hand inputs, for output table
    handsDict = dict(zip(handinputs, pcts))

    return render_template("results.html", handsDict=handsDict, boardinput=boardinput, chop=chop)

