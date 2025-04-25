import RPi.GPIO as GPIO
import time

# === Define motor pins and settings ===
MOTORS = {
    "1": {"DIR": 23, "STEP": 24, "INVERT": False},
    "2": {"DIR": 25, "STEP": 8,  "INVERT": True},
    "3": {"DIR": 7,  "STEP": 12, "INVERT": True},
    "4": {"DIR": 16, "STEP": 20, "INVERT": False},
    "5": {"DIR": 19, "STEP": 26, "INVERT": False, "STEP_DELAY": 0.01}  # Rotary base with slower speed
}

STEP_DELAY = 0.005
STEPS_PER_REV = 400

def setup_pins():
    GPIO.setmode(GPIO.BCM)
    for motor in MOTORS.values():
        GPIO.setup(motor["DIR"], GPIO.OUT)
        GPIO.setup(motor["STEP"], GPIO.OUT)

def step_motor(step_pin, dir_pin, step_count, invert=False, step_delay=STEP_DELAY):
    actual_direction = step_count >= 0
    if invert:
        actual_direction = not actual_direction
    
    GPIO.output(dir_pin, GPIO.HIGH if actual_direction else GPIO.LOW)
    
    for _ in range(abs(step_count)):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(step_delay)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(step_delay)

def step_multiple_motors(motor_ids, step_count):
    delays = {}

    # Set direction for all motors first
    for motor_id in motor_ids:
        motor = MOTORS[motor_id]
        actual_direction = step_count >= 0
        if motor["INVERT"]:
            actual_direction = not actual_direction
        GPIO.output(motor["DIR"], GPIO.HIGH if actual_direction else GPIO.LOW)
        delays[motor_id] = motor.get("STEP_DELAY", STEP_DELAY)

    # Use slowest delay to synchronize all motors
    shared_delay = max(delays.values())

    for _ in range(abs(step_count)):
        for motor_id in motor_ids:
            GPIO.output(MOTORS[motor_id]["STEP"], GPIO.HIGH)
        time.sleep(shared_delay)
        for motor_id in motor_ids:
            GPIO.output(MOTORS[motor_id]["STEP"], GPIO.LOW)
        time.sleep(shared_delay)

def manual_control():
    print("\nManual Control Mode:")
    print("  'w': Move motors 1 and 4 clockwise")
    print("  's': Move motors 1 and 4 counterclockwise")
    print("  'a': Move motors 2 and 3 clockwise")
    print("  'd': Move motors 2 and 3 counterclockwise")
    print("  'e': Rotate motor 5 (rotary base) clockwise")
    print("  'z': Rotate motor 5 (rotary base) counterclockwise")
    print("  't': Compress all motors")
    print("  'g': Release all motors")
    print("  'q': Quit manual control mode")
    
    step_size = 20

    while True:
        cmd = input("\nEnter command (w/a/s/d/e/z/q) or number of steps + command (e.g., '100w'): ").strip().lower()

        if not cmd:
            continue

        digits = ""
        for char in cmd:
            if char.isdigit():
                digits += char
            else:
                break

        if digits:
            try:
                step_size = int(digits)
                cmd = cmd[len(digits):]
            except ValueError:
                print("Invalid step size. Using default.")

        if cmd == 'q':
            print("Exiting manual control mode.")
            break
        elif cmd == 't':
            print("Compressing everything")
            step_multiple_motors(["1", "4", "2", "3"], step_size)
        elif cmd == 'g':
            print("Releasing everything")
            step_multiple_motors(["1", "4", "2", "3"], -step_size)
        elif cmd == 'w':
            print(f"Moving motors 1 and 4 clockwise ({step_size} steps)")
            step_multiple_motors(["1", "4"], step_size)
        elif cmd == 's':
            print(f"Moving motors 1 and 4 counterclockwise ({step_size} steps)")
            step_multiple_motors(["1", "4"], -step_size)
        elif cmd == 'a':
            print(f"Moving motors 2 and 3 clockwise ({step_size} steps)")
            step_multiple_motors(["2", "3"], step_size)
        elif cmd == 'd':
            print(f"Moving motors 2 and 3 counterclockwise ({step_size} steps)")
            step_multiple_motors(["2", "3"], -step_size)
        elif cmd == 'e':
            print(f"Rotating motor 5 clockwise ({step_size} steps)")
            step_multiple_motors(["5"], step_size)
        elif cmd == 'z':
            print(f"Rotating motor 5 counterclockwise ({step_size} steps)")
            step_multiple_motors(["5"], -step_size)
        else:
            print("Invalid command. Please use w/a/s/d/e/z/t/g/q.")

def test_individual_motor():
    print("\nAvailable motors: 1 (Right M1), 2 (Right M2), 3 (Left M2), 4 (Left M1), 5 (Rotational)")
    motor_id = input("Enter motor number to test (or 'q' to quit): ").strip()
    if motor_id.lower() == 'q':
        return
    if motor_id not in MOTORS:
        print("Invalid motor number.")
        return

    direction = input("Enter direction (cw/ccw): ").strip().lower()
    if direction not in ['cw', 'ccw']:
        print("Invalid direction.")
        return

    steps = int(input("Enter number of steps to move: ").strip())
    if direction == 'ccw':
        steps = -steps

    motor = MOTORS[motor_id]
    step_motor(motor["STEP"], motor["DIR"], steps, motor["INVERT"], motor.get("STEP_DELAY", STEP_DELAY))
    print(f"Motor {motor_id} moved {abs(steps)} steps {'clockwise' if steps > 0 else 'counterclockwise'}.")

def main():
    setup_pins()
    try:
        while True:
            print("\nOptions:")
            print("1. Test individual motor")
            print("2. Manual control mode")
            print("q. Quit")
            
            choice = input("Enter your choice: ").strip().lower()
            
            if choice == 'q':
                break
            elif choice == '1':
                test_individual_motor()
            elif choice == '2':
                manual_control()
            else:
                print("Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\nTest interrupted.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
