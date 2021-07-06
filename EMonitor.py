# Based on EMonitor refresh from the C# Code
# Built to operate with a Queue rather than UDP Socket

import pyglet
from multiprocessing import Process, Pipe
# import numpy as np

class EMonitor:
    def __init__(self):
        self.n_sounds = 13

        # Initialize the target forces
        self.target_tor = 1
        self.up_lim_tor = 1
        self.target_tor = 1
        self.match_tor = 1
        self.low_lim_tor = 1

        # Initialize Force Parameters
        self.targetF = 1
        self.up_limF = 1
        self.low_limF = 1
        self.matchF = 1

        self.sound_trigger = [False for i in range(self.n_sounds)]
        self.sounds_playing = list([False for i in range(self.n_sounds)])
        self.players = []

        self.stop_trigger = 0

        self.pipe_end = None

        # Graphics stuff below here
        self.thread_running = True

    def synch_state(self, dt):
        '''
        Validate package size in bytes first
        '''
        io_array = None

        # Clear the buffer and take the most recent datapoint
        while self.pipe_end.poll():
            io_array = self.pipe_end.recv()

        if not io_array:
            return


        # These should all be doubles
        self.target_tor = io_array[0]
        self.low_lim_tor = io_array[1]
        self.up_lim_tor = io_array[2]
        self.match_tor = io_array[3]

        self.targetF = io_array[4]
        self.low_limF = io_array[5]
        self.up_limF = io_array[6]
        self.matchF = io_array[7]

        # This should be an array of booleans
        self.sound_trigger = io_array[8]

        # This should be a single boolean value
        self.stop_trigger = io_array[9]

        # print(self.match_tor, self.matchF)


# Define RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 175)
RED = (255, 0, 0)

SCREEN_INDEX = 1

display = pyglet.canvas.get_display()
screens = display.get_screens()
event_loop = pyglet.app.EventLoop()

if len(screens) >= SCREEN_INDEX:
    print("Using default display")
    SCREEN_INDEX = 0

print(f"{SCREEN_INDEX = }")

# Create objects for the pyglet window and fps display
window = pyglet.window.Window(fullscreen=True, screen=screens[SCREEN_INDEX])
fps_display = pyglet.window.FPSDisplay(window=window)

# set background color as white
pyglet.gl.glClearColor(*WHITE, 255)

# Load the sounds
SOUND_DIRECTORY = "C:\\Users\\pthms\\Desktop\\Local UDP Revamp\\soundCues\\"
FILE_NAMES = ["hold.wav",
              "in.wav",
              "out.wav",
              "match.wav",
              "relax.wav",
              "startingtrial.wav",
              "endingtrial.wav",
              "Out of Range.wav",
              "Wrong Direction.wav",
              "in.wav",
              "out.wav",
              "up.wav",
              "down.wav"]

SOUND_CUES = []
for file in FILE_NAMES:
    n = SOUND_DIRECTORY + file

    print(f"Loading {n}")

    SOUND_CUES.append(pyglet.media.load(n, streaming=False))
print(f"Loaded {len(SOUND_CUES)} sounds successfully")

# Initialize the EMonitor
emonitor = EMonitor()

@event_loop.event
def on_window_close(window):
    print("Hey")
    window.close()
    event_loop.exit()
    return pyglet.event.EVENT_HANDLED

def custom_draw_circle_one_thick(x_center, y_center, radius, color, batch):
    # Implements mid-point circle drawing algorithm

    X = radius
    Y = 0

    points = []

    points.append([X + x_center, y_center])
    points.append([x_center + X, y_center])
    points.append([x_center - X, y_center])

    points.append([x_center, y_center + X])
    points.append([x_center, y_center - X])

    if radius > 0:
        points.append([X + x_center, -Y  + y_center])
        points.append([Y + x_center, X + y_center])
        points.append([-Y + x_center, X + y_center])

    P = 1 - radius

    while X > Y:
        Y += 1

        # Midpoint is inside or on the perimeter
        if P <= 0:
            P = P + 2 * Y + 1

        else:
            X -= 1
            P = P + 2 * Y - 2 * X + 1

        if (X < Y):
            break

        points.append([X + x_center, Y  + y_center])
        points.append([-X + x_center, Y  + y_center])
        points.append([X + x_center, -Y  + y_center])
        points.append([-X + x_center, -Y  + y_center])

        if X != Y:
            points.append([Y + x_center, X  + y_center])
            points.append([-Y + x_center, X  + y_center])
            points.append([Y + x_center, -X  + y_center])
            points.append([-Y + x_center, -X  + y_center])

    num_points = len(points)
    # Concatanate points list; gl expects list in format [x0, y0, x1, y1...]
    collapsed_points = [j for i in points for j in i]

    color_list = color * num_points

    batch.add(num_points,
              pyglet.gl.GL_POINTS,
              None,
              ('v2i', collapsed_points),
              ('c3B', color_list))

def custom_draw_circle(x_center, y_center, radius, color, thickness, batch):
    edges = min(thickness, radius)

    for t in range(edges):
        rad = radius - t

        custom_draw_circle_one_thick(x_center, y_center, rad, color, batch)

def draw_circle(x, y, radius, color, bg_color, thickness, batch):
    a = pyglet.shapes.Circle(x, y, radius, color=color, batch=batch)
    b = None

    if radius - (2*thickness) > 0:
        b = pyglet.shapes.Circle(x, y,
                                 radius - (2 * thickness),
                                 color=bg_color,
                                 batch=batch)

    return [a, b]

def draw_full_line(y, length, color, width, batch):
    return pyglet.shapes.Line(0, y,
                              length, y,
                              width=width,
                              color=color,
                              batch=batch)

@window.event
def on_draw():
    pyglet.clock.tick()

    try:
        WIDTH = window.width
        HEIGHT = window.height

        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Define the radii of the circles
        m = emonitor

        if m.target_tor == 0:
            m.target_tor = 1

        match_target_radius = int(HEIGHT / 1.5)
        lower_range_radius = int(match_target_radius * (m.low_lim_tor / m.target_tor))
        upper_range_radius = int(match_target_radius * (m.up_lim_tor / m.target_tor))
        representation_radius = int(match_target_radius * (m.match_tor / m.target_tor))

        # Code to set the moving Y coordinates
        targetF_line = center_y
        lowF_line = targetF_line * (m.low_limF / m.targetF)
        upF_line = targetF_line * (m.up_limF / m.targetF)

        # The C# Code has matchY = center_y * ((2 - m.matchF) / m.targetF)
        # i'm not sure why the 2.0 - is present though, so I deleted it
        # This might have to be reintroduced sometime
        matchY = center_y * ((m.matchF) / m.targetF)

        window.clear()

        radii = sorted([(match_target_radius, BLACK),
                        (lower_range_radius, BLUE),
                        (upper_range_radius, BLUE)], reverse=True)

        lines = [(lowF_line, BLUE),
                (upF_line, BLUE),
                (matchY, RED),
                (targetF_line, BLACK)]

        batch = pyglet.graphics.Batch()

        # Using a array to hold the graphics objects, to ensure that they
        # aren't destroyed before being drawn

        a = []

        for radius in radii:
            a.append(draw_circle(center_x, center_y, *radius, WHITE, 3, batch))

        for line in lines:
            a.append(draw_full_line(line[0], WIDTH, line[1], 3, batch))

        # My custom drawing function is very slow, so only use it for the
        # moving circle
        batch.draw()

        batch = pyglet.graphics.Batch()
        a.append(custom_draw_circle(center_x, center_y,
                                    representation_radius,
                                    RED, 3, batch))

        fps_display.draw()
        batch.draw()

        # Sound stuff here
        for i in range(emonitor.n_sounds):
            if emonitor.sound_trigger[i] and not emonitor.sounds_playing[i]:
                print(f"Sound {i} is playing")
                emonitor.players.append(SOUND_CUES[i].play())
                emonitor.sounds_playing[i] = True

        if emonitor.stop_trigger:
            print("Stop sounds")
            while emonitor.players:
                emonitor.players.pop().pause()
                emonitor.sounds_playing = [False for i in range(emonitor.n_sounds)]
    except ZeroDivisionError:
        print("Zero division detected")
        pass

def run(interval, conn):
    """Entry"""
    emonitor.pipe_end = conn

    pyglet.clock.schedule_interval(emonitor.synch_state, interval)

    pyglet.app.run()

if __name__ == "__main__":
    pass

