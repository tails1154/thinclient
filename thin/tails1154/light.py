import os
import socket
import RPi.GPIO as GPIO
import time

SOCKET_PATH = "/tmp/indicator_socket"

# GPIO Pin config (BCM numbering)
LED_PINS = {
    "power": 17,
    "warning": 27,
}

# Clean up existing socket
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Indicator states
indicators = {
    "power": False,
    "warning": False,
}

def update_leds():
    for name, state in indicators.items():
        GPIO.output(LED_PINS[name], GPIO.HIGH if state else GPIO.LOW)

def handle_command(cmd):
    parts = cmd.strip().split()
    if len(parts) != 2:
        return
    name, state = parts
    if name in indicators and state in {"on", "off"}:
        indicators[name] = (state == "on")
        update_leds()

# Socket setup
server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server.bind(SOCKET_PATH)

# Main loop
try:
    print("Indicator server running. Send commands like 'power on' to the socket.")
    while True:
        try:
            server.settimeout(0.1)
            data = server.recv(1024).decode()
            handle_command(data)
        except socket.timeout:
            pass
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    server.close()
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

