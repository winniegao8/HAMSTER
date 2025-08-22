import sys
import time
import RPi.GPIO as GPIO

mode=GPIO.getmode()

Forward=29
Backward=31
sleeptime=1
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)

def forward(x):
	GPIO.output(Forward, GPIO.HIGH)
	print("Moving Forward")
	time.sleep(x)
	GPIO.output(Forward, GPIO.LOW)

def reverse(x):
	GPIO.output(Backward, GPIO.HIGH)
	print("Moving Backward")
	time.sleep(x)
	GPIO.output(Backward, GPIO.LOW)

forward(5)
reverse(5)
GPIO.cleanup()
