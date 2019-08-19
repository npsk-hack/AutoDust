from time import sleep
import RPi.GPIO as GPIO
import os

class Control:
    def __init__(self):
        self.pins = [7,8]
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BOARD)
        for pin in self.pins:
            self.GPIO.setup(pin, GPIO.OUT)
        
    def rotate(self, val):
        pin = self.pins[val]
        try:
            self.GPIO.output(pin, GPIO.HIGH)
            sleep(5)
            self.GPIO.output(pin, GPIO.LOW)
            return 1
        except Exception as MotorError:
            print(MotorError)
            return 0

    def capture(self, file_name):
        try:
            os.system("fswebcam -r 1280x720 {}".format(file_name))
            return 1
        except Exception as CamError:
            print(CamError)
            return 0

    def shutdown(self):
        self.GPIO.cleanup()

c = Control()
c.rotate(0)
sleep(2)
c.rotate(1)
