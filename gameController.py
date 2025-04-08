# # -*- coding: utf-8 -*-
# """
# Created on Sun Mar 16 17:19:35 2025
# 
# @author: zacha
# """
# 
# #%%
# """
# Controller physical mappings:
#     button 0: A
#     button 1: B
#     button 2: x
#     button 3: y
#     button 4: left trigger
#     button 5: right trigger
#     button 6: -
#     button 7: + 
#     left joystick: axis 0 (x), axis 1 (y)
#     right joystick: axis 2 (x), axis 3(y)
#     axis 4: left paddle
#     axis 5: right paddle
#     
# """
# 
# 
import pygame
pygame.init()
# 
# if pygame.joystick.get_count() > 0:
#     joystick = pygame.joystick.Joystick(0)
#     joystick.init()
#     print(f"Joystick detected: {joystick.get_name()}")
# else:
#     print("No joystick detected.")
# 
# 
# BUTTON_ACTIONS = {
#     0 : 'open_ee',
#     1 : 'close_ee'
# }
# 
# # Define axis mappings (Axis index → Action)
# AXIS_ACTIONS = {
#     1: ("contract", "expand"),  # Left Stick Y
#     2: ("m2neg", "m2pos"),    # Right Stick X
#     3: ("m1neg", "m1pos"),       # Right Stick Y
#     4: "ccw",                 # LT
#     5: "cw"                 # RT
# }
# 
# DEADZONE = 0.1
# 
# def handle_button_event(button, is_pressed):
#     """Handle button presses"""
#     action = BUTTON_ACTIONS.get(button, "Unknown Button")
#     if is_pressed:
#         print(f"{action} Activated")
#     else:
#         print(f"{action} Released")
# 
# def handle_axis_event(axis, value):
#     """Handles analog stick and trigger movements."""
#     if abs(value) < DEADZONE:
#         return  # Ignore small movements 
# 
#     if axis in [0, 1, 2, 3]:  # Analog Sticks
#         action = AXIS_ACTIONS.get(axis)
#         if action:
#             direction = action[0] if value < 0 else action[1]
#             print(f"{direction} ({value:.2f})")
# 
#     elif axis in [4, 5]:  # Triggers
#         trigger_action = AXIS_ACTIONS.get(axis, "Unknown Axis")
#         print(f"{trigger_action} Pressed: {value:.2f}")
#     
# def main():
#     """Main event loop."""
#     running = True
#     print("in main")
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.JOYBUTTONDOWN:
#                 handle_button_event(event.button, True)
# 
#             elif event.type == pygame.JOYBUTTONUP:
#                 handle_button_event(event.button, False)
# 
#             elif event.type == pygame.JOYAXISMOTION:
#                 handle_axis_event(event.axis, event.value)
# 
#             elif event.type == pygame.QUIT:
#                 running = False
# 
#     pygame.quit()
# 
# if __name__ == "__main__":
#     main()
#%% button tester


# Initialize the first available joystick
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joystick detected!")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")

    print(f"Number of buttons: {joystick.get_numbuttons()}")
    print(f"Number of axes: {joystick.get_numaxes()}")

    # Event loop to read button presses
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released")
            elif event.type == pygame.JOYAXISMOTION:
                print(f"Axis {event.axis} moved to {event.value}")
