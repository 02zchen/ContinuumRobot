import RPi.GPIO as GPIO
import pygame
import time
from gpiozero import PWMOutputDevice, DigitalOutputDevice

# === GPIOZERO CONFIGURATION FOR GRIPPER ===

# TB6612FNG STBY pin (must be HIGH to enable motor driver)
STBY = DigitalOutputDevice(2)
STBY.on()

# Gripper motor pins (Motor A of TB6612FNG)
AIN1 = DigitalOutputDevice(20)  # Direction 1
AIN2 = DigitalOutputDevice(21)  # Direction 2
PWMA = PWMOutputDevice(16, frequency=1000)  # PWM control

# === GPIO SETUP FOR ARM STEPPERS ===

# Arm Stepper Motor 1
DIR_PIN1 = 24
STEP_PIN1 = 25

# Arm Stepper Motor 2
DIR_PIN2 = 8
STEP_PIN2 = 7

STEPS_PER_REV = 400
STEP_DELAY = 0.005

GPIO.setmode(GPIO.BCM)
GPIO.setup([DIR_PIN1, STEP_PIN1, DIR_PIN2, STEP_PIN2], GPIO.OUT)

# === Initialize Pygame and Joystick ===
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

AXIS_MAPPINGS = {0: "Motor1", 3: "Motor2"}

# === Stepper Movement Function ===
def move_motor(step_pin, dir_pin, steps, direction):
    GPIO.output(dir_pin, GPIO.HIGH if direction == "CW" else GPIO.LOW)
    for _ in range(steps):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(STEP_DELAY)

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
