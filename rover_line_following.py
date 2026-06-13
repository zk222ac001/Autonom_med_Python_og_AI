import RPi.GPIO as GPIO
import time

# -------------------
# Opsætning
# -------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

SPEED = 50  # Motorhastighed i procent (0-100)

# -------------------
# Motor pins (PWM)
# -------------------
IN1, IN2, IN3, IN4 = 29, 31, 32, 33
for pin in (IN1, IN2, IN3, IN4):
    GPIO.setup(pin, GPIO.OUT)

pwm_in1 = GPIO.PWM(IN1, 100)
pwm_in2 = GPIO.PWM(IN2, 100)
pwm_in3 = GPIO.PWM(IN3, 100)
pwm_in4 = GPIO.PWM(IN4, 100)
for pwm in (pwm_in1, pwm_in2, pwm_in3, pwm_in4):
    pwm.start(0)

# -------------------
# IR linjesensorer
# -------------------
IR_LEFT = 24
IR_RIGHT = 26
GPIO.setup(IR_LEFT, GPIO.IN)
GPIO.setup(IR_RIGHT, GPIO.IN)

# -------------------
# Motor funktioner
# -------------------
def forward(speed=SPEED):
    pwm_in1.ChangeDutyCycle(speed)   # højre motor
    pwm_in2.ChangeDutyCycle(0)
    pwm_in3.ChangeDutyCycle(speed)   # venstre motor
    pwm_in4.ChangeDutyCycle(0)

def turn_left(speed=SPEED):
    pwm_in1.ChangeDutyCycle(0)
    pwm_in2.ChangeDutyCycle(speed)
    pwm_in3.ChangeDutyCycle(speed)
    pwm_in4.ChangeDutyCycle(0)

def turn_right(speed=SPEED):
    pwm_in1.ChangeDutyCycle(speed)
    pwm_in2.ChangeDutyCycle(0)
    pwm_in3.ChangeDutyCycle(0)
    pwm_in4.ChangeDutyCycle(speed)

def stop():
    pwm_in1.ChangeDutyCycle(0)
    pwm_in2.ChangeDutyCycle(0)
    pwm_in3.ChangeDutyCycle(0)
    pwm_in4.ChangeDutyCycle(0)

# -------------------
# Hovedloop - linjefølger
# -------------------
try:
    print("Starter linjefølger...")
    while True:
        left = GPIO.input(IR_LEFT)   # 0 = sort, 1 = hvid
        right = GPIO.input(IR_RIGHT)

        print(f"IR venstre={left} | IR højre={right}")

        # Logik:
        if left == 0 and right == 0:
            # Begge på sort → fremad
            forward()
        elif left == 0 and right == 1:
            # Venstre på sort → drej venstre
            turn_left()
        elif left == 1 and right == 0:
            # Højre på sort → drej højre
            turn_right()
        else:
            # Begge på hvid → stop
            stop()

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Stopper rover...")
    stop()
    for pwm in (pwm_in1, pwm_in2, pwm_in3, pwm_in4):
        pwm.stop()
    GPIO.cleanup()
