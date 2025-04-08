import RPi.GPIO as GPIO
import time

# Define GPIO pins
DIR_PIN = 24    # Direction pin
STEP_PIN = 25   # Step pin
STEPS_PER_REV = 400  # Adjust based on your motor
STEP_DELAY = 0.001  # 1ms per step pulse

# Setup GPIO
GPIO.setmode(GPIO.BCM)
#GPIO.setup(ENA_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)

def move_motor(steps, direction):
    """Move motor a certain number of steps in given direction"""
    if direction == "CW":
        GPIO.output(DIR_PIN, GPIO.HIGH)  # Set direction CW
    else:
        GPIO.output(DIR_PIN, GPIO.LOW)  # Set direction CCW
    
    time.sleep(0.002)  # Ensure direction change is registered
    
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(STEP_DELAY)

try:
    print("Stepper motor test running...")
    while True:
        move_motor(STEPS_PER_REV, "CW")  # Move forward one revolution
        time.sleep(1)
        move_motor(STEPS_PER_REV, "CCW")  # Move backward one revolution
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping motor...")
    GPIO.cleanup()
