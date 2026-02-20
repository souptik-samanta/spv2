from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

# GPIO pins connected to ROWS
keyboard.row_pins = (board.GP0, board.GP1)

# GPIO pins connected to COLUMNS
keyboard.col_pins = (board.GP2, board.GP3, board.GP4)

# IMPORTANT: Row to Column diode direction
keyboard.diode_orientation = DiodeOrientation.ROW2COL

keyboard.keymap = [
    [
        KC.A, KC.B, KC.C,
        KC.D, KC.E, KC.F
    ]
]

if __name__ == '__main__':
    keyboard.go()