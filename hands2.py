# hands2 adds support for multiple players, although no game situations other than before any cards dealt
# it also adds exception handling for invalid inputs + assert statements in helpers2 to make sure everything works as designed

from helpers import Card, Hand
import random
import time
import sys

# make deck
values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
suits = ['s','h','d','c']
deck = [Card(value, suit) for value in values for suit in suits]
hands = []

# get number of players
try:
    players = int(input("Players: "))
    for i in range(players):
        handinput = input(f"Hand{i+1}: ")
        card1 = Card(f"{handinput[0]}", f"{handinput[1]}")
        card2 = Card(f"{handinput[2]}", f"{handinput[3]}")
        hands.append((card1,card2))
        deck.remove(card1)
        deck.remove(card2)
except (TypeError, ValueError, IndexError):
    print("invalid input!")
    sys.exit(1)

# run simulation (timed, bc it's really slow...)
chop = 0
TRIALS = 100000
winners = [0 for p in range(players)]
start = time.time()
for t in range(TRIALS):
    fullhands = []
    ranks = []
    board = random.sample(deck,5)
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

# calculate and output results
chop = round((chop/TRIALS)*100, 2)
pcts = []
for number in winners:
    pct = round((number / TRIALS) * 100, 2)
    pcts.append(pct)

for a in pcts:
    print(f"Hand{pcts.index(a)+1}: {a}%")

print(f"Chop: {chop}%")
print(round(time.time()-start, 2), "sec")








