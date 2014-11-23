# Implementation of classic arcade game Pong

#  import simpleguitk as simplegui
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = []
ball_vel = []

x0y0 = lambda x: x[0]
x0y1 = lambda x: x[1]
x1y1 = lambda x: x[2]
x1y0 = lambda x: x[3]

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]

    #  horizontal velocity
    ball_vel[0] = -random.randrange(120, 240) / 60 # LEFT
    if direction: ball_vel[0] = random.randrange(120, 240) / 60

    #  vertical velocity: upward
    ball_vel[1] = -random.randrange(60, 180) / 60

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    score1 = score2 = paddle1_vel = paddle2_vel = 0

    # paddle shape
    #  (x0, y0) ------ (x1, y0)
    #           |    |
    #           |    |
    #           |    |
    #           |    |
    #           |    |
    #           |    |
    #  (x0, y1) ------ (x1, y1)

    paddle1_pos = [(0, HEIGHT/2 - HALF_PAD_HEIGHT), # x0, y0
                   (0, HEIGHT/2 + HALF_PAD_HEIGHT), # x0, y1
                   (PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT), # x1, y1
                   (PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT)] # x1, y0

    paddle2_pos = [(WIDTH - PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT), # x0, y0
                   (WIDTH - PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT), # x0, y1
                   (WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT), # x1, y1
                   (WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT)] # x1, y0

    direction = RIGHT
    spawn_ball(direction)


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")


    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # collision detect
    # touch the ceil and bottom, refect immdiately
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # X:P1
    # unbeatable
    if 0 and ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        ball_vel[0] = -ball_vel[0] * 1.1

    if 1 and ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        if ball_pos[1] >= x1y0(paddle1_pos)[1] and ball_pos[1] <= x1y1(paddle1_pos)[1]:
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            # P2 score
            score2 += 1
            spawn_ball(RIGHT)

    # X:P2
    # unbeatable
    if 0 and ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        ball_vel[0] = -ball_vel[0] * 1.1

    if 1 and ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        if ball_pos[1] >= x0y0(paddle2_pos)[1] and ball_pos[1] <= x0y1(paddle2_pos)[1]:
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            # P1 score
            score1 += 1
            spawn_ball(LEFT)

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "Red", "White")

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_vel > 0 and paddle1_pos[1][1] < HEIGHT: # positive
        paddle1_pos = [ (p[0], p[1] + paddle1_vel) for p in paddle1_pos ]
    if paddle1_vel < 0 and paddle1_pos[0][1] > 0: # negative
        paddle1_pos = [ (p[0], p[1] + paddle1_vel) for p in paddle1_pos ]

    if paddle2_vel > 0 and paddle2_pos[1][1] < HEIGHT: # positive
        paddle2_pos = [ (p[0], p[1] + paddle2_vel) for p in paddle2_pos ]
    if paddle2_vel < 0 and paddle2_pos[0][1] > 0: # negative
        paddle2_pos = [ (p[0], p[1] + paddle2_vel) for p in paddle2_pos ]

    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, "White", "Green")
    canvas.draw_polygon(paddle2_pos, 1, "White", "Red")

    # draw scores
    canvas.draw_text(str(score1),[ WIDTH/4, 80 ], 50, "White")
    canvas.draw_text(str(score2),[ WIDTH - WIDTH/4, 80], 50, "White")

ball_vel_bak = []
def keydown(key):
    global paddle1_vel, paddle2_vel

    shift_vel = 5
    # for pad 1
    if key == simplegui.KEY_MAP["w"]: # up
        paddle1_vel -= shift_vel
        #  if not paddle1_vel: paddle1_vel -= 1 # don't stop

    if key == simplegui.KEY_MAP["s"]: # down
        paddle1_vel += shift_vel
        #  if not paddle1_vel: paddle1_vel += 1 # don't stop

    # for pad 2
    if key == simplegui.KEY_MAP["up"]: # up
        paddle2_vel -= shift_vel
        #  if not paddle2_vel: paddle2_vel -= 1 # don't stop

    if key == simplegui.KEY_MAP["down"]: # down
        paddle2_vel += shift_vel
        #  if not paddle2_vel: paddle2_vel += 1 # don't stop

    #################################################
    if key == simplegui.KEY_MAP["r"]:
        new_game()

    global ball_vel, ball_vel_bak
    if key == simplegui.KEY_MAP["p"]:
        ball_vel_bak = ball_vel[:]
        ball_vel = [0, 0]

def keyup(key):
    global paddle1_vel, paddle2_vel

    # for pad 1
    if key == simplegui.KEY_MAP["w"]: # up
        paddle1_vel = 0
        #  if not paddle1_vel: paddle1_vel -= 1 # don't stop

    if key == simplegui.KEY_MAP["s"]: # down
        paddle1_vel = 0
        #  if not paddle1_vel: paddle1_vel += 1 # don't stop

    # for pad 2
    if key == simplegui.KEY_MAP["up"]: # up
        paddle2_vel = 0

    if key == simplegui.KEY_MAP["down"]: # down
        paddle2_vel = 0
        #  if not paddle2_vel: paddle2_vel += 1 # don't stop

    #################################################
    global ball_vel, ball_vel_bak
    if key == simplegui.KEY_MAP["p"]:
        ball_vel = ball_vel_bak[:]

def reset():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset, 100)

# start frame
new_game()
frame.start()
