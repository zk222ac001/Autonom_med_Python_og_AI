# Imports the Raspberry Pi GPIO library and gives it the short name GPIO.
# This library lets Python control the Pi’s pins.
import RPi.GPIO as GPIO
# Imports the standard time module for sleeping and measuring timestamps.
import time
# Disables library warnings (for example, warnings about reusing GPIO channels).
# Handy during development so you don’t get repeated warning messages.
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # using physical PIN numbers

TRIG = 7   # BOARD pin 7 = GPIO4
ECHO = 13  # BOARD pin 13 = GPIO27

# Sets the trigger pin as an output — we send the short pulse out on this pin.
GPIO.setup(TRIG, GPIO.OUT)
# Sets the echo pin as an input — we read the returned pulse on this pin.
GPIO.setup(ECHO, GPIO.IN)

# Starts the function that triggers the sensor, measures the echo pulse length, 
# and converts that to distance.
def measure_distance():
    # Makes sure the TRIG line starts LOW. This is a safe initial state.
    GPIO.output(TRIG, False)
    # Waits 0.2 ms (200 µs) so the sensor and pins settle before sending a pulse.
    time.sleep(0.0002)  # settle
    # Sets TRIG HIGH to start the trigger pulse.
    GPIO.output(TRIG, True)
    # Keeps TRIG HIGH for 10 microseconds — the HC-SR04 needs a ~10 µs pulse to start a measurement.
    time.sleep(0.00001)  # 10 µs pulse
    # Sets TRIG LOW again. The sensor now emits an ultrasonic burst and
    # will pull ECHO HIGH when it receives the echo.
    GPIO.output(TRIG, False)
    # Initialize start_time. It will be set more accurately below when ECHO goes high.
    start_time = time.time()
    # Initialize stop_time.
    stop_time = time.time()
    # Sets a timeout 20 ms into the future. This avoids getting stuck forever if no echo is received.
    # Wait for echo to go high
    timeout = time.time() + 0.02
    # Loop while ECHO is LOW, waiting for the echo to start (ECHO goes HIGH). 
    # time.time() < timeout prevents an infinite loop.
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        # Inside the previous loop we keep updating start_time. The last assigned value
        # (just before ECHO becomes HIGH or timeout) serves as the echo-start timestamp. 
        # (Note: you could instead detect the transition and set start_time once when it 
        # first changes; this repeated-assign method is a simple pattern that works.)
        start_time = time.time()

    # Wait for echo to go low
    # Reset the timeout to 20 ms for the echo HIGH duration. This is another safety guard.
    timeout = time.time() + 0.02
    # Loop while ECHO is HIGH, waiting for it to go LOW again. 
    # The length of this HIGH pulse is proportional to the round-trip travel time of the sound.
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        # Continuously update stop_time while ECHO is HIGH; final value is 
        # the time when the echo pulse ends (or when timeout occurs).
        stop_time = time.time()

    # Calculate distance
    # Compute the duration of the echo pulse in seconds — this is the round-trip time.
    time_elapsed = stop_time - start_time
    # Convert time to distance (centimeters).
    # Speed of sound ≈ 34300 cm/s (343 m/s = 34300 cm/s).
    # time_elapsed * 34300 gives the total distance traveled by the sound (there and back).
    # Divide by 2 to get one-way distance from sensor to object.
    distance = (time_elapsed * 34300) / 2
    # Function returns the measured distance in centimeters.
    return distance

try:
    while True:
        dist = measure_distance()
        print("Distance: {:.1f} cm".format(dist))
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
