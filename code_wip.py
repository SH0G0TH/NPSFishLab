import board
import digitalio
import neopixel
import simpleio
import time
import pwmio
from adafruit_motor import servo, motor

# Initialize LEDs
# LEDs placement on Maker Pi RP2040
LED_PINS = [board.GP0,
            board.GP1,
            board.GP2,
            board.GP3,
            board.GP4,
            board.GP5,
            board.GP6,
            board.GP16,
            board.GP17,
            board.GP26]

LEDS = []
for pin in LED_PINS:
    # Set pins as digital output
    digout = digitalio.DigitalInOut(pin)
    digout.direction = digitalio.Direction.OUTPUT
    LEDS.append(digout)

# Initialize Neopixel RGB LEDs
pixels = neopixel.NeoPixel(board.GP18, 2)
pixels.fill(0)

# Initialize buttons
head = digitalio.DigitalInOut(board.GP7)
tail = digitalio.DigitalInOut(board.GP28)
mouth = digitalio.DigitalInOut(board.GP27)
head.direction = digitalio.Direction.INPUT
tail.direction = digitalio.Direction.INPUT
mouth.direction = digitalio.Direction.INPUT
head.pull = digitalio.Pull.DOWN
tail.pull = digitalio.Pull.DOWN
mouth.pull = digitalio.Pull.DOWN

# Initialize DC motors
m1a = pwmio.PWMOut(board.GP8, frequency=50)
m1b = pwmio.PWMOut(board.GP9, frequency=50)
mouthMotor = motor.DCMotor(m1a, m1b)
m2a = pwmio.PWMOut(board.GP10, frequency=50)
m2b = pwmio.PWMOut(board.GP11, frequency=50)
headTailMotor = motor.DCMotor(m2a, m2b)

# -------------------------------------------------
# ON START: Show running light and play melody
# -------------------------------------------------
for i in range(len(LEDS)):
    LEDS[i].value = True
    time.sleep(0.15)

# Turn off LEDs one-by-one very quickly
for i in range(len(LEDS)):
    LEDS[i].value = False
    time.sleep(0.02)

color = 0x333333

# -------------------------------------------------
# FOREVER LOOP: Check buttons & animate RGB LEDs
# -------------------------------------------------
while True:

    if head.value:
        pixels.fill(0x00FE00)
        headTailMotor.throttle = .25
    elif tail.value:
        pixels.fill(0x0000FF)
        headTailMotor.throttle = -.25
    else:
        headTailMotor.throttle = 0

    if mouth.value:
        mouthMotor.throttle = .25
        pixels.fill(0xFF0000)
    else:
        mouthMotor.throttle = 0

    if not head.value and not tail.value and not mouth.value:
        pixels.fill(color)

    # fill the color on both RGB LEDs

    # Sleep to debounce buttons & change the speed of RGB color swipe
    time.sleep(0.05)