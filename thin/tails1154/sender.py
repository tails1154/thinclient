import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)


try:
   while True:
       e = input("enter 'reboot' to reboot other pi: ")
       if e == "reboot":
         print("Rebooting via gpio")
         GPIO.output(17, GPIO.HIGH)
         print("High output sent")
         time.sleep(5)
         GPIO.output(17, GPIO.LOW)
except KeyboardInterrupt:
   pass
finally:
   GPIO.cleanup()
