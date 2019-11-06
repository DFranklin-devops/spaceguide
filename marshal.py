#!/usr/bin/python
#modified script from http://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/

#Import required Python libraries
import time
import RPi.GPIO as GPIO

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.cleanup()
TRIG = 23
ECHO = 24
GREEN = 17
YELLOW = 27
RED = 22
# Set pins as output and input
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(RED,GPIO.OUT)
#
#

#parking distances in cm
# 172cm=68" 5.5 feet
# 203cm=80" 6.5 feet
dist_warn= 203
dist_stop= 172
#Maximum allowable centimeters to exceed the exact stop distance "dist_stop"
dist_stop_tolerance=8
innerlimit = dist_stop - dist_stop_tolerance
outerlimit = dist_stop + dist_stop_tolerance

def lightson():
    turn_color(GREEN,True)
    turn_color(YELLOW, True)
    turn_color(RED, True)

def lightsoff():
    turn_color(GREEN,False)
    turn_color(YELLOW, False)
    turn_color(RED, False)

def turn_color(color, on):
    GPIO.output(color, on)

def slowblink(color):
    lightsoff()
    turn_color(color,True)
    time.sleep(0.4)
    turn_color(color,False)
    time.sleep(0.5)

def flash(color):
    lightsoff()
    for n in range(5):
        turn_color(color,True)
        time.sleep(0.1)
        turn_color(color,False)
        time.sleep(0.06)

def startup_test():
    #Startup Light test
    turn_color(RED, True)
    time.sleep(0.5)
    turn_color(YELLOW, True)
    time.sleep(0.5)
    turn_color(GREEN,True)
    time.sleep(0.5)
    turn_color(RED, False)
    time.sleep(0.5)
    turn_color(YELLOW, False)
    time.sleep(0.5)
    turn_color(GREEN,False)


def measure():
    # This function measures a distance
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start = time.time()
    while GPIO.input(ECHO)==0:
        start = time.time()
    while GPIO.input(ECHO)==1:
        stop = time.time()
    elapsed = stop-start
    distance = elapsed * 17150
    return round(distance,2)


def calculate_average():
  # This function takes 3 measurements and returns the average.
  dist = []
  for n in range(3):
      dist.append(measure())
      time.sleep(0.07)
  average = sum(dist)/len(dist)
  return average

# Set trigger to False (Low)
GPIO.output(TRIG, False)
lightsoff()
startup_test()
# toggle the trig to start sensor
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

print("Starting ultrasonic distance measure")

sleepcounter = 0
try:

    while sleepcounter < 12:
    #lightsoff()
        distance = calculate_average()
        print("Distance : ", distance)
        if distance > dist_warn:
            slowblink(GREEN)
            print("Keep comin")
        elif distance <= dist_warn and distance > dist_stop + dist_stop_tolerance:
            slowblink(YELLOW)
            print ("Slow down there, ace")
            #elif distance in range(innerlimit,outerlimit):
        elif distance >= innerlimit and distance <= outerlimit:
            lightsoff()
            turn_color(RED, True)
            print("Noice")
            sleepcounter += 1
        elif distance < dist_stop - dist_stop_tolerance:
            flash(RED)
            sleepcounter = 0
            print("Too close")
        else:
            lightsoff()
        time.sleep(0.3)
    lightsoff()
    turn_color(GREEN, True)
    time.sleep(0.5)
    lightsoff()
    GPIO.cleanup()
    print("Good night - now what?")
# now we sleep - driver is parked safely

except KeyboardInterrupt:
    # User pressed CTRL-C
    # Reset GPIO settings
    lightsoff()
    GPIO.cleanup()
