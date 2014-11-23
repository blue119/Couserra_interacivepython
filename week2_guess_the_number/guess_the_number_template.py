# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

#  import simpleguitk as simplegui
import simplegui
import random

secret_number = 0
remaining_num = 10

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    range100()

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global secret_number
    global remaining_num

    secret_number = random.randrange(0, 100)
    remaining_num = 10
    print "New game. Range is from 0 to 100"
    print "Number of remaining guesses is %d" % remaining_num
    print ""

def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global secret_number
    global remaining_num

    secret_number = random.randrange(0, 1000)
    remaining_num = 10
    print "New game. Range is from 0 to 1000"
    print "Number of remaining guesses is %d" % remaining_num
    print ""

def input_guess(guess):
    # main game logic goes here
    global remaining_num

    guess_value = int(guess)
    remaining_num -= 1
    print "Guess was %s" % guess
    print "Number of remaining guesses is %d" % remaining_num

    if guess_value > secret_number:
        print "Higher"
        print ""
    elif guess_value < secret_number:
        print "Lower"
        print ""
    elif guess_value == secret_number:
        print "Correct"
        print ""
        new_game()

    if remaining_num == 0:
        print "Out of remaining number. The number is %d\n" % secret_number
        new_game()

# create frame
frame = simplegui.create_frame("Guess the numbe", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)
frame.start()


# call new_game
new_game()


# always remember to check your completed program against the grading rubric

