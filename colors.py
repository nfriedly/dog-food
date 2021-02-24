"""
NeoPixel Cokor Generators
by Nathan Friedly
Source: https://github.com/nfriedly/circuitpython_neopixel_fader
Based on https://jjmojojjmojo.github.io/time-based-fading.html
"""

import time
import math
import adafruit_fancyled.adafruit_fancyled as fancy


WHITE = fancy.CRGB(255, 255, 255)
BLACK = fancy.CRGB(0, 0, 0)
RED = fancy.CRGB(255, 0, 0)
GREEN = fancy.CRGB(0, 255, 0)
YELLOW = fancy.CRGB(255, 255, 0)
MAGENTA = fancy.CRGB(255, 0, 255)
CYAN = fancy.CRGB(0, 255, 255)
BLUE = fancy.CRGB(0, 0, 255)
ORANGE = fancy.CRGB(255, 127, 0)
VIOLET = fancy.CRGB(139, 0, 255)
INDIGO = fancy.CRGB(46, 43, 95) # todo: make this brighter
PINK = fancy.CRGB(255, 127, 127)
MINT = fancy.CRGB(127, 255, 127)
ROBIN = fancy.CRGB(127, 127, 255)
CANARY = fancy.CRGB(255, 255, 127)

RAINBOW = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET)

class Fader:
    def __init__(self, palette, duration=1.0):
        self.startTime = time.monotonic()
        self.duration = duration
        self.palette = palette
        self.color = 0
        self.changed = False

    def getColor(self):
        # how far along are we in this cycle (in seconds): 0 to duration
        elapsed = (time.monotonic() - self.startTime) % self.duration

        # map elapsed to a float between 0 and the size of the palette
        position = elapsed * (len(self.palette)) / self.duration

        indexA = math.floor(position)
        indexB = math.ceil(position)

        if indexA >= len(self.palette):
            indexA = 0
            indexB = 1
        elif indexB >= len(self.palette):
            indexB = 0

        # grab the colors before and after that position
        colorA = self.palette[indexA]
        colorB = self.palette[indexB]

        # calculate the color at this position inbetween those two
        color = fancy.gamma_adjust(fancy.mix(colorA, colorB, position-indexA)).pack()

        #print("elapsed: {}, position: {}, colorA: {}, colorB: {}, color: {}".format(elapsed, position, colorA, colorB, color))
        return color

    def update(self):
        color = self.getColor()
        self.changed = (color != self.color)
        #print("old color: {}, new color: {}, changed: {}".format(self.color, color, self.changed))
        self.color = color
        return self.changed

class Strober:
    def __init__(self, color=RED, duration=1.0):
        self.startTime = time.monotonic()
        self.duration = duration
        self.peakColor = color
        self.color = 0
        self.changed = False

    def getColor(self):
        # how far along are we in this cycle (in seconds): 0 to duration
        elapsed = (time.monotonic() - self.startTime) % self.duration

        # map elapsed to a float between 0 and the duration
        position = elapsed / self.duration

        # calculate the color at this position inbetween those two
        color = fancy.gamma_adjust(fancy.mix(self.peakColor, BLACK, position)).pack()

        return color

    def update(self):
        color = self.getColor()
        self.changed = (color != self.color)
        #print("old color: {}, new color: {}, changed: {}".format(self.color, color, self.changed))
        self.color = color
        return self.changed