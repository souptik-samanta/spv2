import board
import wifi
import socketpool
import microcontroller
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
import json

# =====================
# KMK SETUP
# =====================
keyboard = KMKKeyboard()

keyboard.row_pins = (board.GP0, board.GP1)
keyboard.col_pins = (board.GP2, board.GP3, board.GP4)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

keyboard.keymap = [
    [
        KC.A, KC.B, KC.C,
        KC.D, KC.E, KC.F
    ]
]

# =====================
# WIFI AP MODE
# =====================
wifi.radio.start_ap(ssid="SouptikKB", password="12345678")

print("AP Started")
print("IP:", wifi.radio.ipv4_address_ap)

pool = socketpool.SocketPool(wifi.radio)

# =====================
# SIMPLE HTTP SERVER
# =====================
server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
server.bind(("0.0.0.0", 80))
server.listen(1)

print("Server Running...")

def send_key_to_pc(key):
    try:
        conn, addr = server.accept()
        request = conn.recv(1024)

        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{key}"
        conn.send(response.encode())
        conn.close()
    except:
        pass

# =====================
# MAIN LOOP
# =====================
while True:
    keyboard.scan()

    for key in keyboard.keys_pressed:
        print("Pressed:", key)
        send_key_to_pc(str(key))
