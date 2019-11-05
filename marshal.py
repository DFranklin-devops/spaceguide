#!/usr/bin/python
#modified script from http://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/

#Import required Python libraries
import time
import RPi.GPIO as GPIO

#GPIO setup
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.cleanup()
TRIG = 4
ECHO = 18
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

#parking distances
dist_warn= 30
dist_stop= 15
#Maximum allowable centimeters to exceed the exact stop distance "dist_stop"
dist_stop_tolerance=3
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

def turn_color(color, on)):
    GPIO.output(color, on)

def slowblink(color):
    lightsoff()
    turn_color(color,True)
    time.sleep(0.4)
    turn_color(color,False)
    time.sleep(0.5)

def fastblink(color):
    lightsoff()
    turn_color(color,True)
    time.sleep(0.2)
    turn_color(color,False)
    time.sleep(0.1)

def hyperblink(color):
    lightsoff()
    for n in range(4):
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
    distance = (elapsed * 34300)/2
    return distance

#def get_distance():
#    GPIO.output(TRIG, True)
#    time.sleep(0.00001)
#    GPIO.output(TRIG, False)
#    while GPIO.input(ECHO) == False:
#        start = time.time()
#    while GPIO.input(ECHO) == True:
#        end = time.time()
#    signal_time = end-start
#    distance = signal_time / 0.000058
#    return distance

def calculate_average():
  # This function takes 3 measurements and returns the average.
  distance = [0]*3
  for n in range(3):
      distance[n]=measure()
      time.sleep(0.1)
  average = sum(distance)/len(distance)
  return average

# Set trigger to False (Low)
GPIO.output(TRIG, False)
lightsoff()
startup_test()

print "Starting ultrasonic distance measure"

sleepcounter = 0
try:

    while sleepcounter < 12:
    #lightsoff()
        distance = calculate_average()
        print "Distance : %.1f" % distance
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
            hyperblink(RED)
            sleepcounter = 0
            print("Too close")
        else:
            lightsoff()
        time.sleep(0.5)
    lightsoff()
    print("Good night - now what?")
#  elseif distance <= distwarn or

except KeyboardInterrupt:
    # User pressed CTRL-C
    # Reset GPIO settings
    lightsoff()
    GPIO.cleanup()
