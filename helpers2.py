# implements Card and Hand classes, allows us to handle poker hand objects and rank them to determine winners
# see design document for details/rationale
# also handles apologies like pset 7

import sys
from flask import redirect, render_template, request, session
from functools import wraps

# Cards have values and suits
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    # stackoverflow for the __eq__ fn because just writing card == card1 didn't work before
    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    # show individual card
    def show(self):
        print(f"{self.value}{self.suit}",end=" ")

# Hands have 2 starting cards and a 5-card board
class Hand:
    # we also create dict objects for count of each value and suit in the hand, for the rank method later on
    def __init__(self, firstcard, secondcard, board):
        self.hand = [firstcard] + [secondcard] + [card for card in board]
        self.values = [card.value for card in self.hand]
        self.suits = [card.suit for card in self.hand]
        self.valuesDict = {value: self.values.count(value) for value in self.values}
        self.suitsDict = {suit: self.suits.count(suit) for suit in self.suits}
        self.valuesSuits = {value: suit for value in self.values for suit in self.suits}

    # show cards in hand
    def showHand(self):
        order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        for card in self.hand:
            card.show()

    # ranks each hand with a hand type and appropriate tiebreakers (see design doc!)
    def rank(self):

        # these ordered lists let us sort by high card
        wrap = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        aceslow = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

        # initialize hand type and values to 0
        handType, handValue, value1, value2, value3, value4 = 0, 0, 0, 0, 0, 0

        # straight flush (5 in order, all same suit)
        for suit in self.suitsDict:
            if self.suitsDict[suit] >= 5:
                s = [f"{card1}s" for card1 in wrap]
                c = [f"{card2}c" for card2 in wrap]
                h = [f"{card3}h" for card3 in wrap]
                d = [f"{card4}d" for card4 in wrap]
                handString = [f"{card.value}{card.suit}" for card in self.hand]

                for suit in [s, c, h, d]:
                    for i in range(10):
                        sfs = set(suit[i:i + 5])
                        handSF = set(handString) & sfs
                        if len(handSF) >= 5:
                            handType = 9

        # quads (4 of one value)
        if handType == 0:
            quadsKickers = []
            for quads in self.valuesDict:
                if self.valuesDict[quads] == 4:
                    handType = 8
                    handValue = order.index(quads)
                    for key in self.valuesDict:
                        if self.valuesDict[key] != 4:
                            quadsKickers.append(key)
                    sortedQuads = sorted(quadsKickers, key=lambda value: order.index(value))
                    value1 = order.index(sortedQuads.pop())

        # boat (3 of one value, 2 of another)
        if handType == 0:
            boatValues = []
            for trips in self.valuesDict:
                if self.valuesDict[trips] == 3:
                    boatValues.append(trips)
            sortedBoat = sorted(boatValues, key=lambda value: order.index(value))
            if len(boatValues) != 0:
                handValue = order.index(sortedBoat.pop())
            if len(boatValues) == 2:
                handType = 7
                value1 = order.index(sortedBoat.pop())
            elif len(boatValues) == 1:
                for pair in self.valuesDict:
                    if self.valuesDict[pair] == 2:
                        handType = 7
                        value1 = order.index(pair)

        # flush (5 cards, all same suit, tiebreaker by high card)
        if handType == 0:
            values = []
            for suit in self.suitsDict:
                if self.suitsDict[suit] >= 5:
                    handType = 6
                    for card in self.hand:
                        if card.suit == suit:
                            values.append(card.value)
                    assert len(values) >= 5
                    sortedFlush = sorted(values, key=lambda value: order.index(value))
                    handValue = order.index(sortedFlush.pop())
                    value1 = order.index(sortedFlush.pop())
                    value2 = order.index(sortedFlush.pop())
                    value3 = order.index(sortedFlush.pop())
                    value4 = order.index(sortedFlush.pop())
                    break

        # straight, tiebreaker by high card
        if handType == 0:
            for i in range(10):
                straights = set(wrap[i:i + 5])
                straightValues = set(self.values) & straights
                if len(straightValues) >= 5:
                    handType = 5
                    if "2" in straightValues:
                        sortedValues = sorted(straightValues, key=lambda value: aceslow.index(value))
                    else:
                        sortedValues = sorted(straightValues, key=lambda value: order.index(value))
                    handValue = order.index(sortedValues.pop())

        # trips/two pair/pair/high card (either 3 of 1 value, 2 of 2 values, 2 of 1 value, high card only)
        if handType == 0:
            tripsValues = []
            pairValues = []
            highCards = []

            # check for pairs and unpaired high cards
            for key in self.valuesDict:
                if self.valuesDict[key] == 3:
                    tripsValues.append(key)
                elif self.valuesDict[key] == 2:
                    pairValues.append(key)
                elif self.valuesDict[key] == 1:
                    highCards.append(key)

            sortedHigh = sorted(highCards, key=lambda value: order.index(value))
            sortedPairs = sorted(pairValues, key=lambda value: order.index(value))

            try:
                if len(tripsValues) == 1:
                    handType = 4
                    handValue = order.index(tripsValues.pop())
                    value1 = order.index(sortedHigh.pop())
                    value2 = order.index(sortedHigh.pop())
                else:
                    if len(pairValues) == 3:
                        handType = 3
                        handValue = order.index(sortedPairs.pop())
                        value1 = order.index(sortedPairs.pop())
                        value2 = max(order.index(sortedPairs.pop()), order.index(sortedHigh.pop()))
                    elif len(pairValues) == 2:
                        handType = 3
                        handValue = order.index(sortedPairs.pop())
                        value1 = order.index(sortedPairs.pop())
                        value2 = order.index(sortedHigh.pop())
                    elif len(pairValues) == 1:
                        handType = 2
                        handValue = order.index(sortedPairs.pop())
                        value1 = order.index(sortedHigh.pop())
                        value2 = order.index(sortedHigh.pop())
                        value3 = order.index(sortedHigh.pop())
                    elif len(pairValues) == 0:
                        handType = 1
                        handValue = order.index(sortedHigh.pop())
                        value1 = order.index(sortedHigh.pop())
                        value2 = order.index(sortedHigh.pop())
                        value3 = order.index(sortedHigh.pop())
                        value4 = order.index(sortedHigh.pop())
            except IndexError:
                print(handType)
                for card in self.hand:
                    card.show()
                sys.exit(1)

        # make sure each hand has a rank
        assert (handType != 0)
        return handType, handValue, value1, value2, value3, value4


# handle apologies (credit to pset7 distribution code)
def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

