import simpleguitk as simplegui

counter = 0

def increment():
    """@todo: Docstring for increment.
    :returns: @todo

    """
    global counter
    counter +=1

def tick():
    """@todo: Docstring for tick.
    :returns: @todo

    """
    increment()
    print counter

def buttonpress():
    """@todo: Docstring for buttonpress.
    :returns: @todo

    """
    global counter
    counter = 0

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("SimpleGUI Test", 100, 100)
timer = simplegui.create_timer(1000, tick)
frame.add_button("Click me", buttonpress)
#  frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
timer.start()

