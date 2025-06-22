import RPi.GPIO as GPIO
import time

BUTTON_PIN = 26  # Change to the pin you’re using

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable internal pull-up

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed!")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()

