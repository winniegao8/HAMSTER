# We imports the GPIO module
import RPi.GPIO as GPIO
# We import the command sleep from time
from time import sleep

# Stops all warnings from appearing
GPIO.setwarnings(False)

# We name all the pins on BOARD mode
GPIO.setmode(GPIO.BOARD)
# Set an output for the PWM Signal
GPIO.setup(12, GPIO.OUT)

# Set up the PWM on pin #16 at 50Hz
pwm = GPIO.PWM(12, 50)


def counterclockwise():
	#pwm.start(0) # Start the servo with 0 duty cycle ( at 0 deg position )
	
	pwm.ChangeDutyCycle(7.5) # Tells the servo to turn to  90 deg position )
	sleep(2) # Tells the servo to Delay for 5sec
	pwm.ChangeDutyCycle(10.3) # Tells the servo to turn to 150 deg position )
	sleep(2) # Tells the servo to Delay for 5sec
	pwm.ChangeDutyCycle(7.5) # Tells the servo to turn to 90 deg position )
	sleep(2) # Tells the servo to Delay for 5sec


def clockwise():
	#pwm.start(0) # Start the servo with 0 duty cycle ( at 0 deg position )
	
	pwm.ChangeDutyCycle(7.5) # Tells the servo to turn to 90 deg position )
	sleep(2) # Tells the servo to Delay for 5sec
	pwm.ChangeDutyCycle(3.7) # Tells the servo to turn to 30 deg position )
	sleep(2) # Tells the servo to Delay for 5sec
	pwm.ChangeDutyCycle(7.5) # Tells the servo to turn to 90 deg position )
	sleep(2) # Tells the servo to Delay for 5sec

def servo_stop():
	pwm.stop(0) # Stop the servo with 0 duty cycle ( at 0 deg position )
	GPIO.cleanup() # Clean up all the ports we've used.

# Main program
pwm.start(0)
clockwise()
counterclockwise()
clockwise()
servo_stop()
