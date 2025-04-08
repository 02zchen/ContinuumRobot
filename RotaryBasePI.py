import RPi.GPIO as GPIO
import pygame
import time

# Define GPIO pins for stepper motor control
DIR_PIN = 24    # Direction pin
STEP_PIN = 25   # Step pin

STEPS_PER_REV = 400  # Adjust based on your motor
STEP_DELAY = 0.005  # 1ms per step pulse

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)

# Initialize Pygame and game controller
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define trigger axis mappings
DEADZONE = 0.1  # Ignore minor movements
TRIGGER_THRESHOLD = 0.5  # Minimum trigger pressure to register action
AXIS_ACTIONS = {2: "CW", 5: "CCW"}  # LT for CW, RT for CCW

# Track trigger states
trigger_states = {2: False, 5: False}

def move_motor(steps, direction):
    """Move motor a certain number of steps in given direction."""
    if direction == "CW":
        GPIO.output(DIR_PIN, GPIO.HIGH)  # Set direction CW
    else:
        GPIO.output(DIR_PIN, GPIO.LOW)  # Set direction CCW
        
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(STEP_DELAY)

def handle_axis_event(axis, value):
    """Handles trigger movements and updates motor direction."""
    if axis in AXIS_ACTIONS:
        # Only set the state to true if the value is greater than the threshold
        if value > TRIGGER_THRESHOLD:
            trigger_states[axis] = True
        else:
            trigger_states[axis] = False

def main():
    """Main event loop for handling game controller input and motor movement."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                handle_axis_event(event.axis, event.value)
            elif event.type == pygame.QUIT:
                running = False
        
        # Move motor based on trigger state
        if trigger_states[2]:  # Left trigger pressed (CW)
            move_motor(int(STEPS_PER_REV*0.0025), "CW")
            time.sleep(0.001)  # Prevent excessive polling
        elif trigger_states[5]:  # Right trigger pressed (CCW)
            move_motor(int(STEPS_PER_REV*0.0025), "CCW")
            time.sleep(0.001)  # Prevent excessive polling

    # Cleanup on exit
    GPIO.cleanup()
    pygame.quit()

if __name__ == "__main__":
    main()
