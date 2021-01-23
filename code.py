"""
Dog food timer
Turns green if the lid to the dog food was opened for > 1 second within the last 8 hours, red otherwise
"""
import time
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull

print("Hello, CircuitPython!")

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

switch = DigitalInOut(board.D2)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

minOpenSeconds = 1
turnRedAfterSeconds = 8 * 60 * 60


# initial state at startup
isOpen = False
lastOpenTime = -1
curOpenTime = -1

while True:
    now = time.monotonic()
    if switch.value:
        # lid is open
        pixels.fill((0, 0, 255))
        if isOpen:
            if now - curOpenTime > minOpenSeconds:
                lastOpenTime = curOpenTime
        else:
            isOpen = True
            curOpenTime = now

    else:
        # lid is closed
        isOpen = False
        if lastOpenTime == -1:
            # unknown state, probably just rebooted
            pixels.fill((0, 0, 255))
        elif now - lastOpenTime > turnRedAfterSeconds:
            pixels.fill((255,0,0))
        else:
            pixels.fill((0, 255, 0))

    time.sleep(0.01)  # debounce delay