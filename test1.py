# import RPi.GPIO as GPIO
# from time import sleep
# 
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(6, GPIO.IN)
# 
# try:
#     print('Waiting for IO12 state cahnges ...')
#     GPIO.wait_for_edge(6, GPIO.RISING)  
#     print('State change detected.')
# except KeyboardInterrupt:
#     GPIO.cleanup()
# 
# GPIO.cleanup()
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

def test_callback(channel):
    print('Event detected.')

print('Waiting for IO12 state cahnges ...')
GPIO.add_event_detect(6, GPIO.RISING, callback=test_callback, bouncetime=300)

try:
    while True:
        sleep(2)
        print('.')
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()