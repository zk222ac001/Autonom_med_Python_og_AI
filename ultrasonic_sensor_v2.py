import RPi.GPIO as GPIO
import time

# -------------------
# GPIO Setup
# -------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbers (BOARD)
# If you want BCM numbering, replace with: GPIO.setmode(GPIO.BCM)

TRIG = 7    # BOARD pin 7 = GPIO4
ECHO = 13   # BOARD pin 13 = GPIO27

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# -------------------
# Measure Distance
# -------------------
def measure_distance():
    # Ensure trigger is LOW
    GPIO.output(TRIG, False)
    time.sleep(0.0002)  # settle time

    # Send a 10 µs HIGH pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)   # 10 µs
    GPIO.output(TRIG, False)

    start_time = time.perf_counter()
    stop_time = time.perf_counter()

    # Wait for ECHO to go HIGH
    timeout = time.perf_counter() + 0.02  # 20 ms timeout
    while GPIO.input(ECHO) == 0:
        start_time = time.perf_counter()
        if start_time > timeout:
            return None  # No echo detected

    # Wait for ECHO to go LOW
    timeout = time.perf_counter() + 0.02
    while GPIO.input(ECHO) == 1:
        stop_time = time.perf_counter()
        if stop_time > timeout:
            return None  # Echo too long → out of range

    # Calculate pulse duration
    time_elapsed = stop_time - start_time
    # Convert to distance (cm): speed of sound = 34300 cm/s
    distance = (time_elapsed * 34300) / 2
    return distance

# -------------------
# Main Loop
# -------------------
try:
    while True:
        dist = measure_distance()
        if dist is None:
            print("No object detected (timeout)")
        else:
            print("Distance: {:.1f} cm".format(dist))
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()

'''...........................................................
Notes for wiring
TRIG pin → Pi pin 7 (GPIO4)
ECHO pin → Pi pin 13 (GPIO27), but via a voltage divider:
ECHO → 1kΩ → GPIO13
ECHO → 2kΩ → GND
VCC → 5V (pin 2 or 4)
GND → Ground (pin 6, 9, 14, etc.)
...............................................................
'''
'''
...........................................................
ECHO pin wiring (voltage divider)
Since the HC-SR04 outputs 5V on ECHO and the Pi GPIO is 3.3V max, you must drop the voltage:
Connect ECHO → 1kΩ resistor → Pi GPIO (ECHO pin)
Connect ECHO → 2kΩ resistor → GND
This forms a simple divider: 5V × (2kΩ / (1kΩ+2kΩ)) ≈ 3.3V ✅ safe for Pi.

'''
