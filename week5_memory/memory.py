# implementation of card game - Memory

import simpleguitk as simplegui
#  import simplegui
import random

FRAME_WIDTH = 800
FRAME_HEIGH = 100
CARD_SIZE = 16
GLOBAL_EXPOSED = False
CLICKED_N = 0

CARD_NUM_MAX = (CARD_SIZE / 2) -1
CARD_WIDTH = FRAME_WIDTH / CARD_SIZE
CARD_HEIGH = FRAME_HEIGH
CARD_COLOR = "Green"
CARDS = []
PREVIUS_CARD = -1
CURRENT_CARD = -1

n_of_card = lambda x: x/CARD_WIDTH

# helper function to initialize globals
def new_game():
    global CARDS, CLICKED_N, PREVIUS_CARD, CURRENT_CARD

    #del old data
    PREVIUS_CARD = -1
    CURRENT_CARD = -1
    CLICKED_N = 0
    CARDS = []
    label.set_text("Turns = %d" % (CLICKED_N/2))

    def _card_place(num):
        """
        return: [[x0, y0], [x0, y1], [x1, y1], [x1, y0],]
        """
        x0 = num * CARD_WIDTH
        x1 = x0 + CARD_WIDTH
        y0 = 0
        y1 = CARD_HEIGH
        return [[x0, y0], [x0, y1], [x1, y1], [x1, y0],]

    cards_number = [ i for _ in xrange(2) for i in xrange(CARD_NUM_MAX+1) ]
    random.shuffle(cards_number)

    for i in xrange(CARD_SIZE):
        card = {}
        card['number'] = cards_number[i]
        card['place'] = _card_place(i)
        card['pass'] = False
        card['exposed'] = False
        CARDS.append(card)

    #  print CARDS

# exposed all cards
#  def exposed():
    #  global GLOBAL_EXPOSED
    #  print "exposed"
    #  if GLOBAL_EXPOSED:
        #  GLOBAL_EXPOSED = False
    #  else:
        #  GLOBAL_EXPOSED = True

# define event handlers
def mouseclick(pos):
    global CLICKED_N, PREVIUS_CARD, CURRENT_CARD, label

    card_n = n_of_card(pos[0])
    # The game ignores clicks on exposed cards.
    if CARDS[card_n]['exposed']: return

    #  print CLICKED_N
    if CLICKED_N and not CLICKED_N % 2:
        # cover all non-pass card
        PREVIUS_CARD = CURRENT_CARD = -1
        for c in CARDS:
            if not c['pass']: c['exposed'] = False

    CLICKED_N += 1
    label.set_text("Turns = %d" % ((CLICKED_N+1)/2))

    # add game state logic here
    CARDS[card_n]['exposed'] = True
    CURRENT_CARD = card_n

    # if current card same as prevoius open, set to pass
    #  Curren 0 7
    #  Previus 2 7
    if PREVIUS_CARD >= 0 and PREVIUS_CARD != CURRENT_CARD:
        if CARDS[CURRENT_CARD]['number'] == CARDS[PREVIUS_CARD]['number']:
            CARDS[CURRENT_CARD]['pass'] = True
            CARDS[PREVIUS_CARD]['pass'] = True

    PREVIUS_CARD = CURRENT_CARD


# cards are logically 50x100 pixels in size
def draw(canvas):
    for card in CARDS:
        number_of_card = n_of_card(card['place'][0][0])
        canvas.draw_text(str(card['number']), (number_of_card * CARD_WIDTH+10, CARD_HEIGH*2/3), 64, 'White')
        if not GLOBAL_EXPOSED and not card['exposed'] and not card['pass']:
            canvas.draw_polygon(card['place'], 3, "White", CARD_COLOR)

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", FRAME_WIDTH, FRAME_HEIGH)
frame.add_button("Reset", new_game)
#  frame.add_button("Exposed", exposed)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
#  frame.set_mousedrag_handler(drag)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric

