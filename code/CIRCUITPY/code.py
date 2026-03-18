import time
import board
import digitalio
import usb_hid
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# RGB setup
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)
pixel.fill((0, 0, 0))

# Each key gets its own color
KEY_COLORS = [
    [(255, 0, 0),    (0, 255, 0),    (0, 0, 255)  ],  # C0: red, green, blue
    [(255, 165, 0),  (128, 0, 255),  (0, 255, 255)],  # C1: orange, purple, cyan
]

COL_PINS = [board.D2, board.D3, board.D6]
ROW_PINS = [board.D0, board.D1]

cols = []
for pin in COL_PINS:
    c = digitalio.DigitalInOut(pin)
    c.direction = digitalio.Direction.OUTPUT
    c.value = True
    cols.append(c)

rows = []
for pin in ROW_PINS:
    r = digitalio.DigitalInOut(pin)
    r.direction = digitalio.Direction.INPUT
    r.pull = digitalio.Pull.UP
    rows.append(r)

kbd = Keyboard(usb_hid.devices)

KEY_MAP = [
    [(Keycode.ZERO,),  (Keycode.ONE,),  (Keycode.TWO,)  ],
    [(Keycode.THREE,), (Keycode.FOUR,), (Keycode.FIVE,) ],
]

DEBOUNCE = 0.05
key_state      = [[False]*3 for _ in range(2)]
last_key_state = [[False]*3 for _ in range(2)]
debounce_time  = [[0.0]*3 for _ in range(2)]

# Glow state
glow_color     = (0, 0, 0)
glow_start     = 0
GLOW_DURATION  = 0.4  # seconds to fade out

def fade(color, t):
    # t goes 0.0 (full) to 1.0 (off)
    return tuple(int(c * (1 - t)) for c in color)

print("Ready!")

while True:
    now = time.monotonic()

    # Update glow fade
    elapsed = now - glow_start
    if elapsed < GLOW_DURATION:
        t = elapsed / GLOW_DURATION
        pixel.fill(fade(glow_color, t))
    else:
        pixel.fill((0, 0, 0))

    for c in range(3):
        cols[c].value = False
        for r in range(2):
            reading = not rows[r].value
            if reading != last_key_state[r][c]:
                debounce_time[r][c] = now
            if (now - debounce_time[r][c]) >= DEBOUNCE:
                if reading and not key_state[r][c]:
                    # Key pressed — trigger glow
                    glow_color = KEY_COLORS[r][c]
                    glow_start = now
                    kbd.press(*KEY_MAP[r][c])
                    time.sleep(0.05)
                    kbd.release_all()
                key_state[r][c] = reading
            last_key_state[r][c] = reading
        cols[c].value = True

    time.sleep(0.005)