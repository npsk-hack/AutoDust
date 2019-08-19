from time import sleep
import RPi.GPIO as GPIO
import os

class Control:
    def __init__(self):
        self.pins = [7,8] #Motor Inteterface Pins
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BOARD)
        for pin in self.pins:
            self.GPIO.setup(pin, GPIO.OUT)
        
    def rotate(self, val):
        pin = self.pins[val]
        try:
            #To Rotate Motor
            self.GPIO.output(pin, GPIO.HIGH)
            sleep(5)
            self.GPIO.output(pin, GPIO.LOW)
            return 1
        except Exception as MotorError:
            print(MotorError)
            return 0

    def capture(self, file_name):
        try:
            alt_cmd = "fswebcam -r 1240x720-v -S 10 --set brightness=50% {}.jpg"
            os.system("fswebcam -r 1280x720 {}".format(file_name)) #To capture image
            return 1
        except Exception as CamError:
            print(CamError)
            return 0

    def shutdown(self):
        self.GPIO.cleanup() #Remove access to GPIO Pins
