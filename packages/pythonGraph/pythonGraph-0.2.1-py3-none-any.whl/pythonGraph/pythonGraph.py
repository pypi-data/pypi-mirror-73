"""

Drawing Operations
==================

pythonGraph's drawing routines can output a variety of shapes in a variety of
colors.

Before using these operations, please note that:

* `open_window` must be called first, otherwise a run-time error will
  occur.
* You must call update_window before the result of the drawing routines will be
  visible on the screen.

Mouse Operations
================

pythonGraph can determine the current location of the mouse.  It can also
determine whether or not a mouse click has occurred.

Before using these operations, please note that:

* `open_window` must be called first, otherwise a run-time error will occur.
* The window must be in focus. If the pythonGraph window is not on top, the
  user may have to click on it once before the application will respond to user
  mouse clicks.

"""

import collections
import math
import random

import pygame


# Pygame Window
win = None

# Pygame events
event_list = []

# Pygame Font ('None' will use the system default)
font = None

# Cache (Used to Prevent Loading the Same Media Multiple Times)
images = {}
sounds = {}

# Color Constants
# Color Lookup
color_lookup = {
   "BLACK": (0, 0, 0),
   "BLUE": (0, 0, 255),
   "BROWN": (153, 76, 0),
   "CYAN": (0, 255, 255),
   "GRAY": (128, 128, 128),
   "GREEN": (0, 128, 0),
   "LIGHT_BLUE": (51, 153, 255),
   "LIGHT_CYAN": (204, 255, 255),
   "LIGHT_GRAY": (224, 224, 224),
   "LIGHT_GREEN": (153, 255, 51),
   "LIGHT_MAGENTA": (255, 153, 204),
   "LIGHT_RED": (255, 102, 102),
   "MAGENTA": (255, 0, 255),
   "RED": (255, 0, 0),
   "WHITE": (255, 255, 255),
   "YELLOW": (255, 255, 0),
   "ORANGE": (255, 165, 0),
}

Color = collections.namedtuple('Color',
                               ['BLACK', 'BLUE', 'BROWN', 'CYAN', 'GRAY',
                                'GREEN', 'LIGHT_BLUE', 'LIGHT_CYAN',
                                'LIGHT_GRAY', 'LIGHT_GREEN', 'LIGHT_MAGENTA',
                                'LIGHT_RED', 'MAGENTA', 'RED', 'WHITE',
                                'YELLOW', 'ORANGE'])

colors = Color(
    BLACK=color_lookup['BLACK'],
    BLUE=color_lookup['BLUE'],
    BROWN=color_lookup['BROWN'],
    CYAN=color_lookup['CYAN'],
    GRAY=color_lookup['GRAY'],
    GREEN=color_lookup['GREEN'],
    LIGHT_BLUE=color_lookup['LIGHT_BLUE'],
    LIGHT_CYAN=color_lookup['LIGHT_CYAN'],
    LIGHT_GRAY=color_lookup['LIGHT_GRAY'],
    LIGHT_GREEN=color_lookup['LIGHT_GREEN'],
    LIGHT_MAGENTA=color_lookup['LIGHT_MAGENTA'],
    LIGHT_RED=color_lookup['LIGHT_RED'],
    MAGENTA=color_lookup['MAGENTA'],
    RED=color_lookup['RED'],
    WHITE=color_lookup['WHITE'],
    YELLOW=color_lookup['YELLOW'],
    ORANGE=color_lookup['ORANGE'])

# Mouse Constants
mouse_lookup = {
    "LEFT": 1,
    "CENTER": 2,
    "RIGHT": 3,
}

MouseButton = collections.namedtuple('MouseButton',
                                     ['LEFT', 'RIGHT', 'CENTER'])
mouse_buttons = MouseButton(
    LEFT=mouse_lookup['LEFT'],
    CENTER=mouse_lookup['CENTER'],
    RIGHT=mouse_lookup['RIGHT'])


# Window Operations
def open_window(width, height):
    '''Creates a graphics window of the specified width and height (in pixels).

    .. note:: You can only have one pythonGraph window open at a time. If you
              attempt to open a second, an error will occur.

    .. note:: The `width` and `height` dimensions cannot be negative.

    The following code snippet opens a 400x300-pixel window:

    .. code-block:: python

        pythonGraph.open_window(400, 300)

    '''
    global win
    pygame.init()
    pygame.mixer.init()
    win = pygame.display.set_mode((width, height))
    clear_window(colors.WHITE)
    set_window_title('pythonGraph')


def close_window():
    '''Closes the pythonGraph window.

    An error is raised if the graphics window is not open.

    .. code-block:: python

        pythonGraph.close_window()

    '''
    quit()


def clear_window(color):
    '''Clears the entire window to a particular color.

    `color` can either be a predefined value (refer to `pythonGraph.colors`) or
    a custom color created using the `create_color` or `create_random_color`
    functions.

    .. code-block:: python

        pythonGraph.clear_window(pythonGraph.colors.RED)

    '''
    color_tuple = _get_color(color)
    win.fill(color_tuple)


def get_window_height():
    width, height = pygame.display.get_surface().get_size()
    return height


def get_window_width():
    width, height = pygame.display.get_surface().get_size()
    return width


def set_window_title(title):
    pygame.display.set_caption(title)


def update_window(refresh_rate=33):
    global event_list
    if win is not None:
        pygame.event.pump()
        del event_list[:]
        pygame.display.update()
        delay(refresh_rate)


# Colors Operations
def create_color(red, green, blue):
    return (red, green, blue)


def create_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return (red, green, blue)


def get_color(x, y):
    return pygame.display.get_surface().get_at((x, y))


def _get_color(color):
    if isinstance(color, str) and str(color).upper() in color_lookup:
        return color_lookup[color.upper()]
    else:
        return color


# Drawing Operations
def _get_rectangle(x1, y1, x2, y2):
    # Assumes that we were given top left / bottom right coordinates (we verify
    # this later)
    top_left_x = x1
    top_left_y = y1
    bottom_right_x = x2
    bottom_right_y = y2

    # Adjusts the coordinates provided so that we know the top left and bottom
    # right
    if y2 < y1:
        top_left_y = y2
        bottom_right_y = y1

    if x2 < x1:
        top_left_x = x2
        bottom_right_x = x1

    return pygame.Rect(top_left_x, top_left_y, bottom_right_x - top_left_x + 1,
                       bottom_right_y - top_left_y + 1)


def draw_arc(x1, y1, x2, y2, start_x, start_y, end_x, end_y, color, width=2):
    """Draw an arc

    Draws the portion of an ellipse that is inscribed inside the given
    rectangle.

    The parameters `(x1, y1)` and `(x2, y2)` represent the two opposite corners
    of the rectangle.

    The arc begins at the intersection of the ellipse and the line passing
    through the center of the ellipse and `(start_x, start_y)`. It then
    proceeds counter-clockwise until it reaches the intersection of the ellipse
    and the line passsing through the center of the ellipse to `(end_x,
    end_y)`.

    `color` can either be a predefined value (refer to `pythonGraph.colors`) or
    a custom color created using the `create_color` or `create_random_color`
    functions.

    `width` is an optional parameter that specifies the "thickness" of the arc
    in pixels. Otherwise, it uses a default value of 2.

    .. code-block:: python

        pythonGraph.open_graph_window(400, 300)
        pythonGraph.draw_arc(1, 100, 200, 1, 250, 50, 2, 2,
                             pythonGraph.colors.BLUE, 3)

    """
    # Creates the bounding rectangle (the rectangle that the arc will reside
    # within
    r = _get_rectangle(int(x1), int(y1), int(x2), int(y2))

    # Calculates the Starting Angle
    start_a = start_x - r.centerx
    start_b = start_y - r.centery
    start_angle = math.atan2(start_b, start_a) * -1.0

    # Calculates the Ending Angle
    end_a = end_x - r.centerx
    end_b = end_y - r.centery
    # the negative makes the arc go counter-clockwise like Raptor
    end_angle = math.atan2(end_b, end_a) * -1.0

    pygame.draw.arc(win, _get_color(color), r, start_angle, end_angle,
                    int(width))


def draw_circle(x, y, radius, color, filled, width=2):
    """Draw a circle

    Draws a circle at `(x, y)` with the specified radius.

    `color` specifies the circle's color. This can either be a predefined value
    (refer to pythonGraph.colors) or a custom color created using the
    create_color function.

    `filled` can be either `True` or `False`, depending on whether or not the
    circle should be filled in or not, respectively.

    `width` is an optional parameter that specifies the width of the circle's
    border. If this value is not provided, a default valueof 2will be
    used.This parameter will be ignoredif `filled` is `True`.

    .. code-block:: python

        pythonGraph.open_window(400, 300)
        pythonGraph.draw_cirlce(200, 150, 50, pythonGraph.colors.GREEN, True)

    """
    global win
    if filled:
        pygame.draw.circle(win, _get_color(color),
                           [int(x), int(y)], int(radius), 0)
    else:
        pygame.draw.circle(win, _get_color(color),
                           [int(x), int(y)], int(radius), int(width))


def draw_ellipse(x1, y1, x2, y2, color, filled, width=2):
    """Draw an ellipse

    Draws anellipse inscribed in the rectangle whose two diagonally opposite
    corners, `(x1, y1)`, `(x2, y2)` are given.

    `color` can either be a predefined value (refer to `pythonGraph.colors`) or
    a custom color created using the `create_color` or `create_random_color`
    functions.

    `filled` can be `True` or `False`, depending on whether or not the ellipse
    is filled in or not, respectively.

    `width` is an optional parameter that specifies the width of the ellipse's
    border. If this value is not provided, a default value of 2 will be used.

    .. code-block:: python

        pythonGraph.open_window(400, 300)
        pythonGraph.draw_ellipse(100, 100, 300, 200,
                                 pythonGraph.colors.BLUE, False, 4)

    """
    global win
    r = _get_rectangle(int(x1), int(y1), int(x2), int(y2))
    if filled:
        pygame.draw.ellipse(win, _get_color(color), r, 0)
    else:
        pygame.draw.ellipse(win, _get_color(color), r, int(width))


def draw_image(filename, x, y, width, height):
    """Draws an image in the pythonGraph window.

    `filename` refers to the name of the file (e.g., "image.png") to be drawn.
    You can use any BMP, JPEG, or PNG file. *The image file should be in the
    same folder as your Python script.*

    `x` and `y` specify the upper-left coordinate where the image is to be
    drawn.

    `width` and `height` represent the desired dimensions of the image.
    pythonGraph will try to scale the image to fit within these dimensions.

    For the following example, assume that the file "falcon.png" exists.

    .. code-block:: python

        pythonGraph.open_graph_window(400, 300)
        pythonGraph.draw_image("falcon.png", 100, 100, 150, 150)

    """
    global win
    _load_image(filename)
    image = pygame.transform.scale(images[filename], (int(width), int(height)))
    win.blit(image, (x, y))


def draw_line(x1, y1, x2, y2, color, width=2):
    """Draws a line segment from `(x1, y1)` to `(x2, y2)`.

    `color` can either be a predefined value (refer to `pythonGraph.colors`) or
    a custom color created using the `create_color` or `create_random_color`

    `width` is an optional parameter that specified the width of the line. If
    this value is not provided, a default value of 2 will be used.

    .. code-block:: python

        pythonGraph.open_window(400, 300)
        pythonGraph.draw_line(50, 50, 300, 250, pythonGraph.colors.BLUE, 3)

    """
    global win
    pygame.draw.line(win, _get_color(color), (int(x1), int(y1)), (int(x2),
                     int(y2)), int(width))


def draw_pixel(x, y, color):
    """Changes the color of a single pixel at location `(x, y)`.

    `color` can either be a predefined value (refer to `pythonGraph.colors`) or
    a custom color breated using the `create_color` or `create_random_color`
    functions.

    .. code-block:: python

        pythonGraph.open_window(400, 300)
        pythonGraph.draw_pixel(50, 50, pythonGraph.colors.RED)
    """
    global win
    win.set_at((int(x), int(y)), _get_color(color))


def draw_rectangle(x1, y1, x2, y2, color, filled, width=2):
    """Draw a rectangle

    Draws a rectangle on the screen.

    `(x1, x2)` is any corner of the rectangle

    `(x2, y2)` is the opposite corner of the rectangle

    `color` specifies the rectangle's color. This can either be a predefined
    value (refer to pythonGraph.colors) or a custom color created using the
    `create_color` function.

    `filled` can be either `True` or `False`, depending on whether or not the
    rectangle should be filled in or not, respectively.

    `width` is an optional parameter that specifies the width of the
    rectangle's border.  If this value is not provided, a default value will be
    used.

    .. code-block:: python

        pythonGraph.open_window(400, 300)
        pythonGraph.draw_rectangle(50, 150, 250, 25,
                                   pythonGraph.colors.RED, True)

    """
    global win
    r = _get_rectangle(int(x1), int(y1), int(x2), int(y2))
    if filled:
        pygame.draw.rect(win, _get_color(color), r, 0)
    else:
        pygame.draw.rect(win, _get_color(color), r, int(width))


# Text Operations
def write_text(text, x, y, color, font_size=30):
    global font
    font = pygame.font.SysFont('None', int(font_size))
    text = font.render(str(text), True, _get_color(color))
    win.blit(text, (int(x), int(y)))


def draw_text(text, x, y, color, font_size=30):
    """Writes the specified text string to the pythonGraph window.

    `text` represents the string to be written.

    `(x, y)` denotes the coordinate of the top left corner of the string.

    `color` can either be a predefined value (refer to `pythonGraph.colors`) or
    a custom color breated using the `create_color` or `create_random_color`
    functions.

    `font_size` is an optional parameter that specifies the size of the text,
    in pixels. If this value is not provided, a default value of 30 will be
    used.

    .. code-block:: python

        pythonGraph.open_window(400, 300)
        pythonGraph.draw_text("Hello, World!", 50, 30,
                              pythonGraph.colors.RED, 50)

    """
    write_text(text, x, y, _get_color(color), font_size)


# Sound
def play_sound_effect(filename):
    _load_sound(filename)
    sound = sounds[filename]
    channel = pygame.mixer.find_channel()  # Searches for an available channel
    if channel is not None:
        channel.play(sound)


def play_music(filename, loop=True):
    pygame.mixer.music.load(filename)

    if loop:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play(1)


def stop_music():
    pygame.mixer.music.stop()


# Events (Keyboard, Mouse, Window)
def _get_events():
    global event_list
    if (len(event_list) == 0):
        event_list = pygame.event.get()
    return event_list


# Event Operations (Keyboard, Mouse, Window)
def get_mouse_x():
    x, y = pygame.mouse.get_pos()
    return x


def get_mouse_y():
    x, y = pygame.mouse.get_pos()
    return y


def _get_mouse_button(button):
    if isinstance(button, str) and str(button).upper() in mouse_lookup:
        return mouse_lookup[button.upper()]
    else:
        return button


def _get_key(key_string):
    # Removes the '[]' characters that surround some keys
    if len(key_string) > 1:
        key_string = key_string.replace("[", "")
        key_string = key_string.replace("]", "")
    return key_string


def key_pressed(which_key):
    for event in _get_events():
        if event.type == pygame.KEYDOWN:
            return _get_key(pygame.key.name(event.key)) == which_key
    return False


def key_down(which_key):
    # Gets the key codes of the pressed keys
    pressed = pygame.key.get_pressed()

    # Converts the key codes into friendly names ('a' instead of 137)
    buttons = [_get_key(pygame.key.name(k))
               for k, v in enumerate(pressed) if v]

    # Checks to see if the desired key is in the array
    return buttons.count(which_key) > 0


def key_released(which_key):
    for event in _get_events():
        if event.type == pygame.KEYUP:
            return _get_key(pygame.key.name(event.key)) == which_key
    return False


def mouse_button_pressed(which_button):
    for event in _get_events():
        if event.type == pygame.MOUSEBUTTONDOWN:
            return event.button == _get_mouse_button(which_button)
    return False


def mouse_button_down(which_button):
    pressed = pygame.mouse.get_pressed()
    return pressed[_get_mouse_button(which_button)-1]


def mouse_button_released(which_button):
    for event in _get_events():
        if event.type == pygame.MOUSEBUTTONUP:
            return event.button == _get_mouse_button(which_button)
    return False


def window_closed():
    if win is None:
        return True
    else:
        for event in _get_events():
            if event.type == pygame.QUIT:
                close_window()
    return win is None


def window_not_closed():
    return not window_closed()


def wait_for_close():
    while not window_closed():
        update_window()


def quit():
    global win
    win = None
    pygame.quit()


# Miscellaneous Operations
def delay(time):
    pygame.time.delay(time)


def get_pressed_key():
    for event in _get_events():
        if event.type == pygame.KEYDOWN:
            return _get_key(pygame.key.name(event.key))
    return None


def _load_image(filename):
    global images
    if filename not in images.keys():
        images[filename] = pygame.image.load(filename).convert_alpha()


def _load_sound(filename):
    global sounds
    if filename not in sounds.keys():
        sound = pygame.mixer.Sound(filename)
        sounds[filename] = sound
