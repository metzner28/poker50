**Poker50: Design**

As a first-order estimate, poker probability is a matter of basic math.
Consider this situation: we have Ace-King of hearts (AhKh, for
consistency with the format used by the calculator) and our opponent has
a pair of queens, QsQc. The board after the turn (with only one card to
come) is Qh2h3dAs. Here, we have a pair of aces and a draw to an
ace-high flush (our hand has 4 hearts), but our opponent has a set
(three of a kind) of queens. Therefore, the only way we win this hand is
by drawing a heart on the river (the last card). There’s no calculator
necessary to find the equity of each hand in this spot: we win if and
only if the last card is a heart, of which there are 13-4 = 9 hearts
left in the deck, out of a possible 52-2 = 50 unknown cards. Therefore,
our win probability is 9/50 or 18% exactly. If every situation were this
simple, there would be no need to design a simulator to find
probabilities -- unfortunately, with (52 choose 5) = 1.7e6 possible
boards assuming all 5 cards are yet to be dealt, we’d need to perform
these calculations for every possible board, in every possible game
situation, to arrive at a probability.

This calculator avoids actually calculating any probabilities, allowing
flexibility in terms of number of players and game situations. No
formulas are hard-coded into the program. Instead, I designed a
simulator that randomly deals 100,000 boards, ranks each player’s final
5-card hand and appropriate tiebreakers (high card, etc., see
documentation for a better explanation of which hand beats which) for
each, and increments a counter for each player when their hand wins.
There were several challenges to this approach, most notably in terms of
speed. Running the simulations takes a non-trivial amount of time that
will definitely be noticed by the user, and any number of simulations
larger than 100,000 took prohibitively long. Luckily, the Law of Large
Numbers ensures that even if we run only 100,000 out of a possible 1.7
million trials, we can be confident in the accuracy of our results as
the win probabilities for each hand converge to the true expectations
relatively quickly. I don’t have the math background to justify this
formally, but some quick research suggests that our algorithm is an
example of a Monte Carlo method, well known in math and programming for
approximating a deterministic problem (there is a finite number of
possible boards, meaning that each hand’s equity is by definition
deterministic) with random sampling. Even 100,000 boards takes a while,
on average about 7-8 sec for 2 players, though, but we sacrifice too
much accuracy (in my judgement) decreasing the number of trials further.

In terms of actual implementation, the calculator is built in Python
using a Flask web framework to make it available online. Cards are
represented via a class with value and suit attributes, and full 7-card
hands are implemented in a Hand class, with attributes for the two cards of
the starting hand and the 5-card board. The Hand class also contains a
“rank” method, which returns a tuple containing the value of a given
hand as well as any “tiebreakers” (by high card, etc). This part of the
calculator was by far the most technically challenging to implement --
Python made running the actual simulations very simple, by comparison.
The rank method takes a 7-card Hand object and assigns it an integer
“hand type” from straight flush (9) to no pair/high card only (1) --
excluding 0 allows us to assert handType != 0 at the end of the method
to ensure that it worked. Also, note that each “check” begins with an if
statement, if handType != 0. This ensures that once a hand is assigned
to a specific type, the calculator doesn’t waste time checking for
lower-valued hands and possibly assigning a hand to a lower type than it
actually has.

To translate between Hand objects and ranks, we start by creating dict
objects that contain each value in a given hand and its corresponding
count, each suit in a given hand and its corresponding count, and the
suit of each value in a hand. For example, then, it’s easy to implement
a check for quads (all 4 of one value + one “kicker) -- basically, for
each value in the “values” dict, check if its corresponding count is 4;
if it is we assign the handType to 8 for quads, look at the highest
value that isn’t 4, and assign “handValue,” or the first “tiebreaker,”
to that value; else we keep going to the next check. The list.index
method (and the question about sorting from the quiz!) came in handy for
finding the highest cards, because we obviously can’t sort lists based
on numbers 2-9 and then some random uppercase letters for the face
cards. Instead, we can make a list called “order” with all values in the
correct order, 2 to A, and sort by order.index. Checking for a flush was
similar: for each suit in the “suits” dict, see if its count is 5, if it
is, flush, then sort the cards in the “values-suits” dict for which the
suit matches, take the highest card and assign its order.index to
handValue, then pop the 4 lower cards from the index-sorted list in
order to get all five high-card “tiebreakers” in case two hands have the
same flush. Implementing the other checks had a very similar thought
process -- I won’t individually explain each one, but it should be
relatively obvious from the code. The only tricky part, algorithmically,
was checking for a straight -- since straights are based on the order of
the cards and not the count of any specific value or suit, we couldn’t
use a dict. Instead, we slice the ordered list of values into all
possible subsets of 5 consecutive elements, convert each and the list of
values in the hand to sets, and check the intersection. If we find an
intersection with at least 5 elements, then we break from the loop
because we’ve found a straight. We then sort the hand values in the set
to find the highest one and pop it to assign handValue to the index of
that element.

Now, hand.rank() returns a tuple (handType, handValue, value1, value2,
value3, value4) which lists, in order, the information needed to
determine who wins a given hand. First, we check the hand type, and the
highest number (best hand) wins. If the hand types are equal, we check
handValue, the “first” relevant tiebreaker, and if those are also equal,
we go to the next tiebreaker, etc, until we’ve checked all five cards if
necessary. With this principle in mind, Python makes implementing the
actual simulator very easy. Within a for loop that repeats 100,000
times, we generate a board by calling random.sample() on the deck,
generate a hand for each player who provided a valid 2-card starting
hand, call hand.rank() on each hand, and store the tuples in a list
where the index of each tuple corresponds to the player whose hand rank
is stored in the tuple. Comparing the hand ranks might seem tricky given
the algorithm above, but luckily tuple comparison in Python works
exactly how we want it to. Calling list.index(max(list)) returns the
index of the “largest” hand rank when each is compared sequentially as
described above, which corresponds to the player with the best hand.
Now, in a separate list, we can create a win counter for each player and
increment the counter at the index of that list corresponding to the
index of the largest tuple, or the winner of the hand. Dividing each
counter by the number of trials (as well as an extra counter for ties,
when max returns more than one tuple), we have a list of simulated win
probabilities for each player. We now zip this list together with the
list of hand inputs and create a dict, in order to use Jinja as in pset7
to output an html table of starting hands and their corresponding
equities.