import RPi.GPIO as GPIO
import time
# import the library
from RpiMotorLib import RpiMotorLib
try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    #define GPIO pins
    GPIO_pins = (13, 19, 26) # Microstep Resolution MS1-MS3 -> GPIO Pin
    direction= 21       # Direction -> GPIO Pin
    step = 20     # Step -> GPIO Pin

    # Declare an named instance of class pass GPIO pins numbers
    mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")


    # call the function, pass the arguments
    mymotortest.motor_go(False, "Full" , 200, .1, False, .01)
# time.sleep(2)
#     GPIO.setup(21, GPIO.OUT, initial = GPIO.LOW)#dir
#     GPIO.setup(20, GPIO.OUT, initial = GPIO.LOW)#pul
# #             time.sleep(0.025)
# #             GPIO.output(38, GPIO.HIGH)
# #             time.sleep(0.00025)
#     pwm = GPIO.PWM(20, 100)
#     pwm.start(50)
#     time.sleep(2)
#     pwm.stop()
finally:
    GPIO.cleanup()
