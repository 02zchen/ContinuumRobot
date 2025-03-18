import serial
import pygame
import time

#Note that this code is for computer and arduino based communication. 

# Initialize pygame and joystick
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Set up serial connection to Arduino
try:
    ser = serial.Serial('COM5', 9600, timeout=1)  # Adjust COM port as needed
    print("Controller connected. Hold LT for 'A' and RT for 'D'.")
except serial.SerialException as e:
    print(f"Error: {e}")
    ser = None

# Define constants
DEADZONE = 0.1  # Ignore minor movements
TRIGGER_THRESHOLD = 0.5  # Minimum trigger pressure to register action
COMMAND_DELAY = 0.1  # Delay between sending commands (prevents spamming)

# Define trigger axis mappings
AXIS_ACTIONS = {
    4: b'A',  # Left Trigger (LT) → 'A'
    5: b'D'   # Right Trigger (RT) → 'D'
}

# Track trigger states
trigger_states = {4: False, 5: False}

def handle_axis_event(axis, value):
    """Handles trigger movements and sends serial commands while held."""
    if axis in AXIS_ACTIONS:
        if value > TRIGGER_THRESHOLD:
            trigger_states[axis] = True  # Mark trigger as pressed
        else:
            trigger_states[axis] = False  # Mark trigger as released

def main():
    """Main event loop."""
    running = True
    last_sent_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                handle_axis_event(event.axis, event.value)
            elif event.type == pygame.QUIT:
                running = False

        # Continuously send command while trigger is pressed
        current_time = time.time()
        if current_time - last_sent_time > COMMAND_DELAY:
            for axis, is_pressed in trigger_states.items():
                if is_pressed and ser:
                    ser.write(AXIS_ACTIONS[axis])
                    print(f"Sent {AXIS_ACTIONS[axis].decode()} to Arduino")
            last_sent_time = current_time

    # Close serial connection on exit
    if ser and ser.is_open:
        ser.close()
    pygame.quit()

if __name__ == "__main__":
    main()
