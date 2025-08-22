# DC motor
import RPi.GPIO as GPIO
import pigpio
import time
# Controller
import evdev
import numpy as np

from time import sleep
import pigpio



# Dc Motor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)

pinOneMotor_pwm = GPIO.PWM(29, 10000)
pinTwoMotor_pwm = GPIO.PWM(31, 10000)  # PWM pin

pinOneMotor_pwm.start(0)
pinTwoMotor_pwm.start(0)

# Servo
servo = 18
#GPIO.setup(12, GPIO.OUT)
#servo_pwm = GPIO.PWM(12,50)
#servo_pwm.start(0)

servo_pwm = pigpio.pi()
servo_pwm.set_mode(servo, pigpio.OUTPUT)
servo_pwm.set_PWM_frequency(servo, 50)


# Controller
def map_value(value, in_min, in_max, out_min, out_max):
    return np.interp(value, [in_min, in_max], [out_min, out_max])
device = evdev.InputDevice('/dev/input/event4')
print(device)

# Motor control methods
def forward(speed):
    print(f"Going Forward at {speed}%")
    GPIO.output(31, False)
    pinOneMotor_pwm.ChangeDutyCycle(speed)

def backward(speed):
    print(f"Going Backward at {speed}%")
    GPIO.output(29, False)
    pinTwoMotor_pwm.ChangeDutyCycle(speed)

# def servo(speed):
# #    print(f"Turning at {speed}")
    # GPIO.output(12, False)
    # servo_pwm.ChangeDutyCycle(speed)


try:
    # Event loop
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            # L Joystick
            if event.code == evdev.ecodes.ABS_Y:
                speed = round(map_value(event.value, 0, 31000, 100, 0))
                print(f"Up: {event.value}")
                forward(speed)
            if event.code == evdev.ecodes.ABS_Y:
                speed = round(map_value(event.value, 35000, 65535, 0, 100))
                print(f"Down: {event.value}")
                backward(speed)
            # R Joystick
            if event.code == evdev.ecodes.ABS_Z:
                val = event.value
                if val <= 15000:
                    servo_pwm.set_servo_pulsewidth(servo, 750) ;                
                if 15000 < val <= 30000:
                    servo_pwm.set_servo_pulsewidth(servo, 1125) ;
                if 30000 < val <= 35000:
                    servo_pwm.set_servo_pulsewidth(18, 1500);
                if 35000 < val <= 50000:
                    servo_pwm.set_servo_pulsewidth(18, 1875);
                if val > 50000:
                    servo_pwm.set_servo_pulsewidth(18, 2250);
                # if val <= 30000:
                    # val = 30000
                    # print(f"Left: {val}")
                    # #print(f"Turning at {speed}")
                    # servo(6)
                # elif 30000 < val < 35000:
                    
                    # print(f"Center: {event.value}")
                    # servo(7.5)
                # elif val >= 35000:
                    # val = 35000
                    # print(f"Right: {val}")
                    # servo(9)
            #sleep(0.2)
                # if val <= 31000:
                    # speed = round(map_value(event.value, 0, 33000, 5, 7.5))
                    # print(f"Left: {event.value}")
                    # servo(speed)
                    
                # elif val >= 35000:
                    # speed = round(map_value(event.value, 35000, 65535, 7.5, 10))
                    # print(f"Right: {event.value}")
                    # servo(speed)
#                elif val > 31000 and val < 35000:
#                    speed = 0
#                    servo(speed)


except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
