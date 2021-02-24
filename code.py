"""
Dog food timer
Turns green if the lid to the dog food was opened for > 1 second within the last 8 hours, red otherwise
"""
import time
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import colors

print("Dog food timer initializing...")

rgb = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.5, auto_write=True)

switch = DigitalInOut(board.D2)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

minOpenSeconds = 1
turnRedAfterSeconds = 8 * 60 * 60


# states (does circuitpython support enums?)
UNKNOWN = 0
SHORT_OPEN = 1
LONG_OPEN = 2
FED = 3
HUNGRY = 4

# initial state at startup
isOpen = False
lastOpenTime = -1
curOpenTime = -1
colorGenerator = colors.Strober(color=colors.BLUE, duration=1)
prevState = UNKNOWN

while True:
    now = time.monotonic()
    state = prevState

    # first calculate the state
    if switch.value:
        # lid is open
        if isOpen:
            if now - curOpenTime > minOpenSeconds:
                lastOpenTime = curOpenTime
                state = LONG_OPEN
        else:
            isOpen = True
            curOpenTime = now
            state = SHORT_OPEN
    else:
        # lid is closed
        isOpen = False
        if lastOpenTime == -1:
            # unknown state, probably just rebooted
            state = UNKNOWN
        elif now - lastOpenTime > turnRedAfterSeconds:
            state = HUNGRY
        else:
            state = FED

    # if the state has changed, swap in a new colorGenerator
    if state != prevState:
        #print("state changed from {} to {}".format(prevState, state))
        prevState = state
        if state == SHORT_OPEN:
            print("Lid is open")
            # fade from blue (door is open) to red (start of rainbow)
            colorGenerator = colors.Fader((colors.BLUE, colors.RED), duration=1)
        elif state == LONG_OPEN:
            print("Lid has been open long enough to assume the dog has been fed")
            # rainbow
            colorGenerator = colors.Fader(colors.RAINBOW, duration=3)
        elif state == FED:
            print("The dog has been fed")
            # green breathing
            colorGenerator = colors.Fader((colors.GREEN, colors.BLACK), duration=6)
        elif state == HUNGRY:
            print("Time to feed the dog")
            # red strobe
            colorGenerator = colors.Strober(color=colors.RED, duration=1)
        else:
            # unknown
            colorGenerator = colors.Strober(color=colors.BLUE, duration=1)

    if colorGenerator.update():
        rgb.fill(colorGenerator.color)

    frameTime = time.monotonic() - now

    time.sleep(1/60 - frameTime)  # target 60FPS
