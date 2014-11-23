# http://www.codeskulptor.org/#user38_hkRBzjqExU_6.py
# template for "Stopwatch: The Game"
import simplegui

# define global variables
counter = 0
matched = 0
tried = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minutes = int(t)/600
    seconds = (int(t)%600)/10
    tos = int(t)%10
    return "%d:%.2d.%d" % (minutes, seconds, tos)

# Timer handler
def tick():
    global counter
    counter += 1
    #print format(counter)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    global matched
    global tried
    
    if timer.is_running(): tried += 1
    if timer.is_running() and counter and not (counter % 10): matched += 1
    timer.stop()
    
def reset():
    global counter
    global matched
    global tried
    counter = 0
    matched = 0
    tried = 0
    timer.stop()

# define event handler for timer with 0.1 sec interval
timer = simplegui.create_timer(100, tick)

# define draw handler
def draw(canvas):
    canvas.draw_text(format(counter), [40, 110], 64, "White")
    canvas.draw_text("%d/%d" % (matched, tried), [160, 40], 36, "Green")

# create frame
frame = simplegui.create_frame("stopwatch", 230, 150)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# start frame
frame.start()
#timer.start()

