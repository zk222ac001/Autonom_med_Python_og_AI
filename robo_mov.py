# import libraries ............
import time
import RPi.GPIO as GPIO
# GPIO settings .................
GPIO.setwarnings(False)
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

class robot:
    # Constructor
    def __init__(self,name,rwheel,lwheel):
        self.name = name
        # Getting GPIO's setting for R's and L's , tuple data structure to store collection of data
        self.rwheel = tuple(rwheel)
        self.lwheel = tuple(lwheel)
        # identifing ind #s as input
        # right wheel forward
        self.rwheel_f = int(rwheel[0])
         # right wheel backward
        self.rwheel_b = int(rwheel[1])
        # left wheel forward
        self.lwheel_f = int(lwheel[0])
         # left wheel backward
        self.lwheel_b = int(lwheel[1])
    # Method
    def forward(self,s):
        GPIO.output(self.rwheel_f,True)
        GPIO.output(self.lwheel_f,True)
        #STOP
        time.sleep(s)
        GPIO.output(self.rwheel_f,False)
        GPIO.output(self.lwheel_f,False)

    def backward(self,s):
        GPIO.output(self.rwheel_b,True)
        GPIO.output(self.lwheel_b,True)
        #STOP
        time.sleep(s)
        GPIO.output(self.rwheel_b,False)
        GPIO.output(self.lwheel_b,False)

    def left_turn(self,s):
        GPIO.output(self.rwheel_f,True)
        #STOP
        time.sleep(s)
        GPIO.output(self.rwheel_f,False)

    def right_turn(self,s):
        GPIO.output(self.lwheel_f,True)
        #STOP
        time.sleep(s)
        GPIO.output(self.lwheel_f,False)

# object initialization and pass input pins ( 29,31,32,33) as a tuple
robby = robot("robby",(29,31),(32,33))
print(robby.name , robby.rwheel, robby.lwheel, robby.rwheel_f, robby.lwheel_f)
robby.forward(3)
robby.backward(3)
robby.left_turn(3)
robby.right_turn(3)
