import time
import RPi.GPIO as GPIO

# GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Define pins
IN1 = 29   # Right motor forward
IN2 = 31   # Right motor backward
IN3 = 32   # Left motor forward
IN4 = 33   # Left motor backward

# Setup pins as outputs
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Motor control functions
def motor_a_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def motor_a_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

def motor_b_forward():
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def motor_b_backward():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def forward():
    motor_a_forward()
    motor_b_forward()

def backward():
    motor_a_backward()
    motor_b_backward()

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Main program
try:
    while True:
        print("Moving forward...")
        forward()
        time.sleep(3)   # Move forward for 3 seconds

        print("Moving backward...")
        backward()
        time.sleep(3)   # Move backward for 3 seconds

        print("Stopping...")
        stop()
        time.sleep(2)   # Stop for 2 seconds

# Press Ctrl + c to stop the program
except KeyboardInterrupt:
    print("Exiting program")
    stop()
    GPIO.cleanup()
