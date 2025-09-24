# DC motor
import RPi.GPIO as GPIO
import pigpio
import time
# Controller
import evdev
import numpy as np

from time import sleep
import pigpio

motor_file = open("\home\hamster\motor_rpm.csv", "a")
pendulum_file = open("\home\hamster\pendulum_angle.csv", "a")

# Dc Motor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

pinOneMotor_pwm = GPIO.PWM(8, 10000)
pinTwoMotor_pwm = GPIO.PWM(10, 10000)  # PWM pin

pinOneMotor_pwm.start(0)
pinTwoMotor_pwm.start(0)

voltage = 10

# Servo
servo = 12
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
    GPIO.output(10, False)
    pinOneMotor_pwm.ChangeDutyCycle(speed)
    

def backward(speed):
    print(f"Going Backward at {speed}%")
    GPIO.output(8, False)
    pinTwoMotor_pwm.ChangeDutyCycle(speed)


try:
    # Event loop
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            # L Joystick
            if event.code == evdev.ecodes.ABS_Y:
                percent = round(map_value(event.value, 0, 31000, 100, 0))
                speed = percent *.01 * 5 * voltage
                print(f"Forward: {speed} RPM")
                forward(speed)
                motor_file.write(f"{time.strftime('%M:%S')},{speed}\n")
                motor_file.flush()
            if event.code == evdev.ecodes.ABS_Y:
                percent = round(map_value(event.value, 35000, 65535, 0, 100))
                speed = percent *.01 * 5 * voltage
                print(f"Backward: {speed} RPM")
                backward(speed)
                motor_file.write(f"{time.strftime('%M:%S')},{speed}\n")
                motor_file.flush()
            # R Joystick
            if event.code == evdev.ecodes.ABS_Z:
                val = event.value
                if val <= 15000:
                    servo_pwm.set_servo_pulsewidth(servo, 833.3) ; # 30 deg   
                    angle = 30
                if 15000 < val <= 30000:
                    servo_pwm.set_servo_pulsewidth(servo, 1166.67) ; # 60 deg
                    angle = 60
                if 30000 < val <= 35000:
                    servo_pwm.set_servo_pulsewidth(18, 1500); # 90 deg center
                    angle = 90
                if 35000 < val <= 50000:
                    servo_pwm.set_servo_pulsewidth(18, 1833.3); # 120 deg
                    angle = 120
                if val > 50000:
                    servo_pwm.set_servo_pulsewidth(18, 2166.67); # 150 deg
                    angle = 150
                pendulum_file.write(f"{time.strftime('%M:%S')},{angle}\n")
                pendulum_file.flush()
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


except KeyboardInterrupt:
    pass
finally:
    motor_file.close()
    pendulum_file.close()
    GPIO.cleanup()
