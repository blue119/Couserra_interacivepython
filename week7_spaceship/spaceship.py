# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
SHIP_FRICTION = 0.05
DEBUG = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3") missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

SHIP_DIRECTION = 0
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.start_pos = [0, 0]
        self.move_dist = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        if not self.thrust:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
        else:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size, self.pos, self.image_size, self.angle)

    def shoot(self):
        global a_missile
        if DEBUG: print 'shoot'
        _v = angle_to_vector(self.angle)
        _pos = [self.pos[0] + _v[0] * self.image_center[0], self.pos[1] + _v[1] * self.image_center[1]]
        _vel = [self.vel[0] + 6 * _v[0], self.vel[1] + 6 * _v[1]]
        a_missile = Sprite(_pos, _vel, self.angle, self.angle_vel, missile_image, missile_info, missile_sound)

    def update(self):
        self.angle += SHIP_DIRECTION

        # Pos Update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # Friction Update
        self.vel[0] *= (1 - SHIP_FRICTION)
        self.vel[1] *= (1 - SHIP_FRICTION)

        # Thrust Updae
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0]
            self.vel[1] += forward[1]

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel

        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT


def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # Draw Score
    canvas.draw_text("Lives", [50, 50], 32, "White")
    canvas.draw_text("Score", [680, 50], 32, "White")
    canvas.draw_text(str(lives), [50,  80], 32, "White")
    canvas.draw_text(str(score), [680, 80], 32, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    if a_missile: a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    if a_missile: a_missile.update()

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

def ship_key_up(key_id):
    global SHIP_DIRECTION

    if key_id == simplegui.KEY_MAP['left']:
        SHIP_DIRECTION = 0

    elif key_id == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        ship_thrust_sound.rewind()

    elif key_id == simplegui.KEY_MAP['right']:
        SHIP_DIRECTION = 0

def ship_key_down(key_id):
    global SHIP_DIRECTION

    if key_id == simplegui.KEY_MAP['left']:
        SHIP_DIRECTION = -0.1

    elif key_id == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        ship_thrust_sound.play()

    elif key_id == simplegui.KEY_MAP['right']:
        SHIP_DIRECTION = 0.1

    elif key_id == simplegui.KEY_MAP['space']:
        my_ship.shoot()

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started

    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    _pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    _vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    _avel = random.random() * .2 - .1
    if DEBUG: print "a_rock_pos %s" % str(_pos)
    a_rock = Sprite(_pos, _vel, 0, _avel, asteroid_image, asteroid_info)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
#my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0, 0], 0, 0.1, asteroid_image, asteroid_info)

#                 (pos,                             vel,   ang, ang_vel, image, info, sound = None):
a_missile = None
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)


# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(ship_key_up)
frame.set_keydown_handler(ship_key_down)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

