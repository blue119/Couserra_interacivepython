# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
busted_num = 21

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

DECK = None
# Players
DEALER = None
DEALER_CARD_POS = [50, 200]
BACK_CARD_POS = [DEALER_CARD_POS[0] + CARD_BACK_CENTER[0], CARD_BACK_CENTER[1] + DEALER_CARD_POS[1]]

PLAYER = None
PLAYER_CARD_POS = [50, 400]


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self._cars = [] # create Hand object

    def __str__(self):
        return "Hand contains %s" % ' '.join([str(c) for c in self._cars])  # return a string representation of a hand

    def add_card(self, card):
        self._cars.append(card) # add a card object to a hand

    def _num_ace_card(self):
        return sum([1 for c in self._cars if VALUES[str(c)[1]] == 1])

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        v = sum([VALUES[c.get_rank()] for c in self._cars])

        for _ in range(self._num_ace_card()):
            if v <= 21 - 10: v += 10

        return v

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        # self._cars[0].draw(canvas, pos)
        n = 0
        for c in self._cars:
            c.draw(canvas, [pos[0] + n * CARD_SIZE[0], pos[1]])
            n += 1

# define deck class
class Deck:
    def __init__(self):
        self._deck = [ Card(s, r) for s in SUITS for r in RANKS ] # create a Deck object

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self._deck)    # use random.shuffle()

    def deal_card(self):
        return self._deck.pop() # deal a card object from the deck

    def __str__(self):
        # return a string representing the deck
        return "Deck contains %s" % ' '.join([str(c) for c in self._deck])

def state():
    global outcome, in_play, DECK, PLAYER, DEALER

    print "=" * 20 + " STAT " + "=" * 20
    print 'Dealer(%d): %s' % (DEALER.get_value(), str(DEALER))
    print 'Player(%d): %s' % (PLAYER.get_value(), str(PLAYER))
    print DECK
    print "in_play: " + str(in_play)
    print "outcome: " + outcome
    print "score: %d" % score
    print

#define event handlers for buttons
def deal():
    global score, outcome, in_play, DECK, PLAYER, DEALER

    # your code goes here
    if in_play:
        score -= 1
        outcome = "You Lose."
        in_play = False
        return

    # 1. shuffle the deck
    DECK = Deck()
    DECK.shuffle()
    print DECK

    # 2. create new player and dealer hands
    DEALER = Hand()
    PLAYER = Hand()

    # 3. add two cards to each hand
    DEALER.add_card(DECK.deal_card())
    PLAYER.add_card(DECK.deal_card())

    DEALER.add_card(DECK.deal_card())
    PLAYER.add_card(DECK.deal_card())

    outcome = ""
    in_play = True
    state()

def hit():
    global score, outcome, in_play, DECK, PLAYER, DEALER
    if not in_play: return

    # if the hand is in play, hit the player
    PLAYER.add_card(DECK.deal_card())

    # if busted, assign a message to outcome, update in_play and score
    if PLAYER.get_value() > 21:
        outcome = "You went bust and lose."
        in_play = False
        score -= 1
        print outcome

    state()

def stand():
    global score, outcome, in_play, DECK, PLAYER, DEALER

    if not in_play: return

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while True:
            if DEALER.get_value() >= 17: break
            DEALER.add_card(DECK.deal_card())

        DV = DEALER.get_value()
        PV = PLAYER.get_value()
        # assign a message to outcome, update in_play and score
        if PV <= 21 and (PV > DV or DV > 21):
            outcome = "You Win."
            score += 1
        else:
            outcome = "You Lose."
            score -= 1
        in_play = False

    state()

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [130, 100], 64, "Red")
    canvas.draw_text("Score %d" % score, [400, 100], 40, "White")

    canvas.draw_text("Dealer", [50, 180], 40, "Black")
    canvas.draw_text(outcome,  [210, 180], 40, "Black")
    DEALER.draw(canvas, DEALER_CARD_POS)

    if in_play: canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, BACK_CARD_POS, CARD_BACK_SIZE)

    canvas.draw_text("Player", [50, 380], 40, "Black")
    canvas.draw_text("Hit or Stand?" if in_play else "New deal?",  [210, 380], 40, "Black")

    PLAYER.draw(canvas, PLAYER_CARD_POS)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric>

