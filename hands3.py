# final version on the command line

from helpers import Card, Hand
import random
import time
import sys

values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
suits = ['s','h','d','c']
deck = [Card(value, suit) for value in values for suit in suits]
hands = []

try:
    players = int(input("Players: "))
    for i in range(players):
        handinput = input(f"Hand{i+1}: ")
        card1 = Card(f"{handinput[0]}", f"{handinput[1]}")
        card2 = Card(f"{handinput[2]}", f"{handinput[3]}")
        hands.append((card1,card2))
        deck.remove(card1)
        deck.remove(card2)
except TypeError:
    print("invalid number of players!")
    sys.exit(1)
except (ValueError, IndexError):
    print("invalid cards!")
    sys.exit(1)

try:
    boardinput = input(f"Board (if any): ")
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
            print("invalid board!")
            sys.exit(1)

except (ValueError,IndexError):
    print("invalid board!")
    sys.exit(1)

chop = 0
TRIALS = 100000
winners = [0 for p in range(players)]
start = time.time()
for t in range(TRIALS):
    fullhands = []
    ranks = []

    if len(boardinput) == 6:
        board = [board1, board2, board3] + random.sample(deck,2)
    elif len(boardinput) == 8 and board4:
        board = [board1, board2, board3, board4] + random.sample(deck,1)
    else:
        sys.exit(1)

    for h in hands:
        hand = Hand(h[0], h[1], board)
        fullhands.append(hand)
    for f in fullhands:
        rank = f.rank()
        ranks.append(rank)
    assert len(ranks) == players
    if ranks.count(max(ranks)) != 1:
        chop += 1
    else:
        win = ranks.index(max(ranks))
        winners[win] += 1

chop = round((chop/TRIALS)*100, 2)
pcts = []
for number in winners:
    pct = round((number / TRIALS) * 100, 2)
    pcts.append(pct)

for a in pcts:
    print(f"Hand{pcts.index(a)+1}: {a}%")

print(f"Chop: {chop}%")
print(round(time.time()-start, 2), "sec")
