#importing functions for code
import RPi.GPIO as GPIO
from time import sleep
from SGD_Sound import *
from message import *

#function to create message recipients
def alert_customers():
    R1=Message("+13186697942", "HIGHLY COMBUSTABLE GAS LEVELS DETECTED!")
    R2=Message("+15044069132", "HIGHLY COMBUSTABLE GAS LEVELS DETECTED!")
    R3=Message("+13182336216", "HIGHLY COMBUSTABLE GAS LEVELS DETECTED!")
    receivers=[R1,R2,R3]
    for i in receivers:
            i.send()
    for i in receivers:
            del i


###this section is for setup and basic starting function
#sets up lights for appropriate output types
def set_up(lights):
    GPIO.setmode(GPIO.BCM) #setting pins to appropriate IO types
    GPIO.setwarnings(False)
    for i in lights:
        GPIO.setup(i, GPIO.OUT)

def clean():
    GPIO.cleanup()


#function to turn all lights on
def on_all(lights):
    for i in lights:
        GPIO.output(i, GPIO.HIGH)

        
#function to turn all lights off
def off_all(lights):
    set_up(lights)
    for i in lights:
        GPIO.output(i, GPIO.LOW)


#FUNCTIONS FOR  DIFFERENT ALARM STATUSS
#function for normal status
def normal_lights(green_leds):
    #ensure lights and pins are set up corectly
    set_up(green_leds)
    on_all(green_leds)


def danger_lights(red_leds):
    timer=60
    set_up(red_leds)
    play_annoying_sound()
    alert_customers()
    while(timer > 1):
        on_all(red_leds)
        sleep(0.2)
        off_all(red_leds)
        sleep(0.2)
        timer-=1

