import RPi.GPIO as GPIO
import pygame
import time
from gpiozero import PWMOutputDevice, DigitalOutputDevice

# === GPIOZERO CONFIGURATION FOR GRIPPER ===

# Gripper TB6612FNG pins
STBY = DigitalOutputDevice(2) # green upper left
STBY.on() # must be high to enable 
AIN1 = DigitalOutputDevice(20)  # Direction 1, second from bottom right
AIN2 = DigitalOutputDevice(21)  # Direction 2, bottom right 
PWMA = PWMOutputDevice(16, frequency=1000)  # PWM control

# === GPIO SETUP FOR ARM STEPPERS ===

# Arm Stepper Motor 1, right module 1
DIR_PIN1 = 23
STEP_PIN1 = 24

# Arm Stepper Motor 2, right module 2
DIR_PIN2 = 25
STEP_PIN2 = 8

#Arm Stepper Motor 3, left module 2  
DIR_PIN3 = 7
STEP_PIN3 = 12

#Arm Stepper Motor 4, left module 1 
DIR_PIN4 = 16
STEP_PIN4 = 20

#global stepping params 
STEPS_PER_REV = 400
STEP_DELAY = 0.005

GPIO.setmode(GPIO.BCM)
GPIO.setup([DIR_PIN1, STEP_PIN1, DIR_PIN2, STEP_PIN2, DIR_PIN3, STEP_PIN3, DIR_PIN4, STEP_PIN4], GPIO.OUT)

# === Initialize Pygame and Joystick ===
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

AXIS_MAPPINGS = {0: "Motor1", 3: "Motor2", }

# === Stepper Movement Function ===
def step_motor(step_pin, dir_pin, step_count):
    direction = GPIO.HIGH if step_count >= 0 else GPIO.LOW
    GPIO.output(dir_pin, direction)
    for _ in range(abs(step_count)):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(STEP_DELAY)
        
def control_module1(axis_value):
    """
    Upper module. To move right, reel in the right tendon while releasing the left equally.
    """
    steps = int(STEPS_PER_REV * 0.0025)
    if axis_value > 0.1:  # Right
        step_motor(STEP_PIN1, DIR_PIN1, steps)   # Right tendon pulls in
        step_motor(STEP_PIN4, DIR_PIN4, -steps)  # Left tendon slacks out
    elif axis_value < -0.1:  # Left
        step_motor(STEP_PIN1, DIR_PIN1, -steps)  # Right tendon slacks out
        step_motor(STEP_PIN4, DIR_PIN4, steps)   # Left tendon pulls in

def control_module2(axis_value):
    """
    
    """
    steps = int(STEPS_PER_REV * 0.0025)
    if axis_value > 0.1:
        step_motor(STEP_PIN2, DIR_PIN2, steps)   # Right tendon pulls in
    elif axis_value < -0.1:
        step_motor(STEP_PIN3, DIR_PIN3, steps)   # Left tendon pulls in


# === Gripper Motor Control ===
def control_gripper(opening=False, closing=False):
    if opening:
        AIN1.on()
        AIN2.off()
        PWMA.value = 1.0
    elif closing:
        AIN1.off()
        AIN2.on()
        PWMA.value = 1.0
    else:
        AIN1.off()
        AIN2.off()
        PWMA.value = 0

# === Main Loop ===
def main():
    print("Joystick control started. Press Ctrl+C to quit.")
    try:
        while True:
            pygame.event.pump()

            # Stepper control
            for axis in AXIS_MAPPINGS:
                value = joystick.get_axis(axis)
                if abs(value) > 0.1:
                    steps = int(STEPS_PER_REV * 0.0025)
                    direction = "CW" if value > 0 else "CCW"
                    if axis == 0:
                        move_motor(STEP_PIN1, DIR_PIN1, steps, direction)
                    elif axis == 3:
                        move_motor(STEP_PIN2, DIR_PIN2, steps, direction)

            # Gripper control
            gripper_open = joystick.get_button(0)   # A button
            gripper_close = joystick.get_button(1)  # B button
            control_gripper(opening=gripper_open, closing=gripper_close)

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()
        pygame.quit()

if __name__ == "__main__":
    main()
