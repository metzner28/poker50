**Poker50: Documentation**

Poker50 is a simulator and equity calculator for Texas Hold 'Em, a very
popular type of poker played everywhere from small home games to casinos
and nationally televised tournaments. In Texas Hold 'Em, each player is
dealt two cards face-down; then three cards are dealt face-up; then one
card face-up; and finally, another one face up. Each deal is separated
by a round of betting. The object of the game is to win the pot by
making the best 5-card poker hand from any combination of the two
face-down private cards and five face-up “community cards.” Hands are
ranked in order of increasing rarity, or decreasing probability --
making probability a central concept in poker and the basis for this
equity simulator.

Given any number of players from 2 to 9 inclusive, their individual
two-card starting hands, and any “game situation,” i.e. zero, three, or
four community cards already dealt, the calculator returns an HTML table
of equities -- win probabilities -- for each individual hand after a
full board of five community cards is dealt. For context: the best hand
in poker is a straight flush, of which there are only 40 combinations
(we count 10 "straights" of 5 cards increasing sequentially, from A2345
to TJQKA, for each of four suits) out of a possible (52 choose 5) =
1.7x10^6 possible hands. After that, hand types decrease in value with
four of a kind (4 of one value and 1 extra "kicker"), full house (three
of one value and two of another), flush (any five cards of the same
suit), straight (any 5 cards increasing sequentially), three of a kind
(three of one value, 2 extra “kickers”), two pair (two pairs of values,
one extra), and one pair (two of the same value, three extra kickers).
Hands of the same value, as well as all other hands that don’t fit into
these categories, are ranked based on their highest card, with aces
counting either high or low for straights and straight flushes -- and
again, the highest ranked hand wins. The calculator runs 100,000 board
simulations, keeps track of each winner, and divides each total by the
number of trials to return the equity percentages for each player.

Usage is very straightforward: first, the user types in an integer
number of players and clicks “Next,” which links to an HTML form with
fields for each player’s hand and a board, if any. The user inputs cards
by typing into an HTML form as “{VALUE}{suit}” where {VALUE} is an
element in [2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A] and {suit} is in
[s, h, d, c]. The cards are case-sensitive: values must be numbers or
uppercase letters, suits must be lowercase, and no spaces or other
characters separate values and suits, or one card from the other. For
example, the starting hand Ace-King of hearts would be represented AhKh,
while community cards (“a board”) of, say, 9 of hearts/10 of hearts/2 of
clubs would be typed in as 9hTh2c. After clicking “Run,” the calculator
should run the simulations and return an HTML table displaying win
probabilities for each 2-card starting hand. The calculator throws
“invalid cards” or “invalid board” apologies if it cannot convert the
string of user input into Card objects, or remove all inputted cards
from the deck before dealing and running the simulations. This can
happen if user input includes unrecognized characters (say the user
types ‘a’ instead of ‘s’ for a card’s suit) or if a card is repeated
(i.e. one player inputs AhAc and another inputs AhKh -- the Ace of
Hearts can’t be used twice here). Output is similarly simple and clean:
the calculator returns an html table of starting hands and their
equities in the given situation, as well as an extra line “Chop”
indicating the probability of a tie (“Chop” in poker means “chop up the
pot,” or split it between two or more hands because of a tie). Overall,
the calculator was designed to be a simple and uncluttered alternative
to existing poker equity calculators, which are usually filled with ads
and hard to use.

Since the project uses the Flask web framework, it should be
straightforward to get it up and running online once downloaded to the
CS50 IDE (or wherever it might be opened). For me, simply typing “cd
project flask run” gives a URL (that I set to public) allowing access.
Feel free to run hands1.py/hands2.py/hands3.py, but these are just
command-line drafts of the code for the calculator itself. The final
product lives in application.py and runs through Flask, with html
templates in the templates directory and CSS borrowed from pset7 in the
static directory. Apologies are also borrowed from pset7.