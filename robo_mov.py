# import libraries ............
import time
#Imports the RPi.GPIO library (used for controlling Raspberry Pi GPIO pins) and aliases it as GPIO.
import RPi.GPIO as GPIO
# GPIO settings .................
# Disables warning messages from the GPIO library.
GPIO.setwarnings(False)
# Sets the GPIO pin numbering mode to physical pin numbers (not Broadcom SOC channel numbers).
GPIO.setmode(GPIO.BOARD)

# Labeling all pins but GND is output.........
# GPIO Board is physical pins
print("program start...")
# 29 - brown - R forward
GPIO.setup(29,GPIO.OUT)
# 31 - green - R backward
GPIO.setup(31,GPIO.OUT)
# 32 - yellow - L forward
GPIO.setup(32,GPIO.OUT)
# 33 - blue - L backward
GPIO.setup(33,GPIO.OUT)

# Defines a class called robot.
class robot:
    #  __init__: Constructor method, called when an object is created.
    def __init__(self,name,rwheel,lwheel):
        self.name = name
        # Getting GPIO's setting for R's and L's , tuple data structure to store collection of data
        # Stores right wheel pins as a tuple.
        self.rwheel = tuple(rwheel)
        # Stores left wheel pins as a tuple.
        self.lwheel = tuple(lwheel)
        # The next lines extract individual pin numbers from the tuples
        # Right wheel forward pin.
        self.rwheel_f = int(rwheel[0])
         # right wheel backward PIN
        self.rwheel_b = int(rwheel[1])
        # left wheel forwards single pin
        self.lwheel_f = int(lwheel[0])
         # left wheel backward single pin
        self.lwheel_b = int(lwheel[1])
    # Method
    def forward(self,s):
        # Turns on both forward pins for right and left wheel.
        GPIO.output(self.rwheel_f,True)
        GPIO.output(self.lwheel_f,True)
        
        # Sleeps for s seconds (robot moves forward).
        time.sleep(s)
        # Turns off both pins (stops movement).
        GPIO.output(self.rwheel_f,False)
        GPIO.output(self.lwheel_f,False)

    def backward(self,s):
        # Turns on both backward pins.
        GPIO.output(self.rwheel_b,True)
        GPIO.output(self.lwheel_b,True)
        
        time.sleep(s)
        #STOP Turn off the bons
        GPIO.output(self.rwheel_b,False)
        GPIO.output(self.lwheel_b,False)

    def left_turn(self,s):
        # Turns on only the right wheel forward pin.
        GPIO.output(self.rwheel_f,True)
        #STOP
        time.sleep(s)
        GPIO.output(self.rwheel_f,False)

    def right_turn(self,s):
        # Turns on only the left wheel forward pin.
        GPIO.output(self.lwheel_f,True)
        #STOP
        time.sleep(s)
        GPIO.output(self.lwheel_f,False)


# Creates an instance of the robot class named "robby" with right wheel pins (29, 31) 
# and left wheel pins (32, 33).
robby = robot("robby",(29,31),(32,33))
print(robby.name , robby.rwheel, robby.lwheel, robby.rwheel_f, robby.lwheel_f)
robby.forward(3)
robby.backward(3)
robby.left_turn(3)
robby.right_turn(3)
