import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set GPIO pin 18 as an output pin
GPIO.setup(18, GPIO.OUT)

try:
    while True:
        GPIO.output(18, GPIO.HIGH)  # Turn on the LED
        time.sleep(1)               # Wait for 1 second
        GPIO.output(18, GPIO.LOW)   # Turn off the LED
        time.sleep(1)               # Wait for 1 second

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
