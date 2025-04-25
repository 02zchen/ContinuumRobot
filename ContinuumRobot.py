# Controller physical mappings (DO NOT DELETE)
#     button 0: A
#     button 1: B
#     button 2: X
#     button 3: Y
#     button 4: left trigger
#     button 5: right trigger
#     button 6: -
#     button 7: + 
#     left joystick: axis 0 (x) ? module 1
#     right joystick: axis 3 (y) ? module 2
#     axis 2: left paddle ? rotary base CCW
#     axis 5: right paddle ? rotary base CW

import RPi.GPIO as GPIO
import pygame
import time

# === GPIO SETUP ===
AIN1 = 4
AIN2 = 22
PWMA = 27
STBY = 17

DIR_PIN1 = 23
STEP_PIN1 = 24
DIR_PIN2 = 25
STEP_PIN2 = 8
DIR_PIN3 = 7
STEP_PIN3 = 12
DIR_PIN4 = 16
STEP_PIN4 = 20
DIR_PIN5 = 19
STEP_PIN5 = 26

STEPS_PER_REV = 400
STEP_DELAY = 0.001

# === GPIO INIT ===
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup([AIN1, AIN2, PWMA, STBY,
            DIR_PIN1, STEP_PIN1, DIR_PIN2, STEP_PIN2,
            DIR_PIN3, STEP_PIN3, DIR_PIN4, STEP_PIN4,
            DIR_PIN5, STEP_PIN5], GPIO.OUT)
GPIO.output(STBY, GPIO.HIGH)

# === Pygame INIT ===
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# === Axis Indexes ===
AXIS_MODULE1 = 0      # Left joystick X
AXIS_MODULE2 = 3      # Right joystick Y
AXIS_ROTARY_LEFT = 2  # Left paddle
AXIS_ROTARY_RIGHT = 5 # Right paddle

# === Motor Direction Multipliers ===
MOTOR_DIR_MULTIPLIERS = {
    STEP_PIN1: 1,
    STEP_PIN2: -1,
    STEP_PIN3: -1,
    STEP_PIN4: 1,
    STEP_PIN5: 1
}

# Rotary base position tracking
rotary_position_deg = 0
DEGREES_PER_STEP = 360 / STEPS_PER_REV

# === Stepper Utility ===
def step_motor(step_pin, dir_pin, step_count):
    direction = GPIO.HIGH if step_count * MOTOR_DIR_MULTIPLIERS.get(step_pin, 1) >= 0 else GPIO.LOW
    GPIO.output(dir_pin, direction)
    for _ in range(abs(step_count)):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(STEP_DELAY)

# === Movement Control Functions ===
def control_module1(axis_value):
    steps = int(STEPS_PER_REV * 0.01 * abs(axis_value))
    if axis_value > 0.1:
        step_motor(STEP_PIN1, DIR_PIN1, steps)
        step_motor(STEP_PIN4, DIR_PIN4, int(-0.5*steps))
    elif axis_value < -0.1:
        step_motor(STEP_PIN1, DIR_PIN1, int(-0.5*steps))
        step_motor(STEP_PIN4, DIR_PIN4, steps)

def control_module2(axis_value):
    steps = int(STEPS_PER_REV * 0.01 * abs(axis_value))
    if axis_value > 0.1:
        step_motor(STEP_PIN2, DIR_PIN2, steps)
        step_motor(STEP_PIN3, DIR_PIN3, int(-0.5*steps))
    elif axis_value < -0.1:
        step_motor(STEP_PIN2, DIR_PIN2, int(-0.5*steps))
        step_motor(STEP_PIN3, DIR_PIN3, steps)

def control_rotary_base(left_val, right_val):
    global rotary_position_deg

    steps_per_press = int(STEPS_PER_REV * 0.005)
    degrees_per_press = steps_per_press * DEGREES_PER_STEP

    if right_val > 0.9 and rotary_position_deg + degrees_per_press <= 720:
        step_motor(STEP_PIN5, DIR_PIN5, steps_per_press)
        rotary_position_deg += degrees_per_press

    elif left_val > 0.9 and rotary_position_deg - degrees_per_press >= -720:
        step_motor(STEP_PIN5, DIR_PIN5, -steps_per_press)
        rotary_position_deg -= degrees_per_press

def control_gripper(opening=False, closing=False):
    if opening:
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(PWMA, GPIO.HIGH)
    elif closing:
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(PWMA, GPIO.HIGH)
    else:
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(PWMA, GPIO.LOW)

def compress_module1():
    steps = int(STEPS_PER_REV * 0.02)
    step_motor(STEP_PIN1, DIR_PIN1, steps)
    step_motor(STEP_PIN4, DIR_PIN4, steps)

def compress_module2():
    steps = int(STEPS_PER_REV * 0.02)
    step_motor(STEP_PIN2, DIR_PIN2, steps)
    step_motor(STEP_PIN3, DIR_PIN3, steps)

def extend_module1():
    steps = int(STEPS_PER_REV * 0.02)
    step_motor(STEP_PIN1, DIR_PIN1, -steps)
    step_motor(STEP_PIN4, DIR_PIN4, -steps)

def extend_module2():
    steps = int(STEPS_PER_REV * 0.02)
    step_motor(STEP_PIN2, DIR_PIN2, -steps)
    step_motor(STEP_PIN3, DIR_PIN3, -steps)

# === Main Control Loop ===
def main():
    print("Joystick control started. Press Ctrl+C to quit.")
    try:
        while True:
            pygame.event.pump()

            # Rotary base paddle control
            control_rotary_base(
                joystick.get_axis(AXIS_ROTARY_LEFT),
                joystick.get_axis(AXIS_ROTARY_RIGHT)
            )

            # Module controls
            module1_val = joystick.get_axis(AXIS_MODULE1)
            if abs(module1_val) > 0.1:
                control_module1(module1_val)

            module2_val = joystick.get_axis(AXIS_MODULE2)
            if abs(module2_val) > 0.1:
                control_module2(module2_val)

            # Button-based compression and extension
            if joystick.get_button(2):  # X button
                compress_module1()
            if joystick.get_button(3):  # Y button
                compress_module2()
            if joystick.get_button(0):  # A button
                extend_module1()
            if joystick.get_button(1):  # B button
                extend_module2()

            # Gripper trigger control
            gripper_open = joystick.get_button(4)  # Left Trigger
            gripper_close = joystick.get_button(5)  # Right Trigger
            control_gripper(opening=gripper_open, closing=gripper_close)

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()
        pygame.quit()

if __name__ == "__main__":
    main()
