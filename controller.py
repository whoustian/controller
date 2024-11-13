import pygame
from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key
import time
import math

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()

# Set up the controller
if pygame.joystick.get_count() < 1:
    print("No controller connected.")
    exit()


controller = pygame.joystick.Joystick(0)
controller.init()
print(f"Controller connected: {controller.get_name()}")

# Mouse controller
mouse = Controller()

# Initialize keyboard controller
keyboard = KeyboardController()

# Mouse sensitivity and deadzone settings
base_sensitivity = 3  # Adjust for base speed
deadzone = 0.05  # Ignore small movements
smoothing_factor = 0.1  # Lower for faster response

# Sensitivity for scrolling
scroll_sensitivity = 1  # Adjust this for faster/slower scrolling

# Threshold for L2 and R2 press
trigger_threshold = 0.5  # Move this outside the loop for better readability

# Initialize position deltas for smooth movement
x_velocity = 0
y_velocity = 0
l2_press = False
r2_press = False

# Sensitivity scaling function
def exponential_sensitivity(raw_value, base_sensitivity, exponent=1):
    """
    Apply exponential sensitivity scaling.
    A higher exponent will make the sensitivity more drastic.
    """
    return base_sensitivity * math.pow(abs(raw_value), exponent)

try:
    while True:
        # Poll events
        for event in pygame.event.get():
            # Handle JOYAXISMOTION for mouse control
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:  # Left stick X-axis          
                    raw_x = event.value
                    # Apply dynamic sensitivity based on joystick intensity
                    if abs(raw_x) > deadzone:
                        scaled_sensitivity_x = exponential_sensitivity(raw_x, base_sensitivity)
                        x_velocity = (raw_x * scaled_sensitivity_x) * smoothing_factor + x_velocity * (1 - smoothing_factor)
                    else:
                        x_velocity = 0  # Reset to zero within deadzone
                elif event.axis == 1:  # Left stick Y-axis
                    raw_y = event.value
                    # Apply dynamic sensitivity based on joystick intensity
                    if abs(raw_y) > deadzone:
                        scaled_sensitivity_y = exponential_sensitivity(raw_y, base_sensitivity)
                        y_velocity = (raw_y * scaled_sensitivity_y) * smoothing_factor + y_velocity * (1 - smoothing_factor)
                    else:
                        y_velocity = 0  # Reset to zero within deadzone

                # Scrolling with Right Stick
                # Right stick X-axis (horizontal scrolling)
                if event.axis == 2:
                    raw_x = event.value
                    if abs(raw_x) > deadzone:  # Only scroll if joystick is being pressed
                        # Apply smoothing and scaling to the x-axis movement
                        right_stick_x_velocity = (raw_x * scroll_sensitivity) * smoothing_factor + right_stick_x_velocity * (1 - smoothing_factor)
                        # Scroll horizontally
                        mouse.scroll(-right_stick_x_velocity, 0)
                    else:
                        # If joystick is in the neutral zone, stop scrolling
                        right_stick_x_velocity = 0

                # Right stick Y-axis (vertical scrolling)
                elif event.axis == 3:
                    raw_y = event.value
                    if abs(raw_y) > deadzone:  # Only scroll if joystick is being pressed
                        # Apply smoothing and scaling to the y-axis movement
                        right_stick_y_velocity = (raw_y * scroll_sensitivity) * smoothing_factor + right_stick_y_velocity * (1 - smoothing_factor)
                        # Scroll vertically
                        mouse.scroll(0, right_stick_y_velocity)
                    else:
                        # If joystick is in the neutral zone, stop scrolling
                        right_stick_y_velocity = 0

                # Handle L2 and R2 (Triggers as buttons)
                elif event.axis == 4:  # L2
                    if event.value > trigger_threshold:
                        l2_press = True
                    else:
                        l2_press = False

                elif event.axis == 5:  # R2
                    if event.value > trigger_threshold:
                        r2_press = True
                    else:
                        r2_press = False


            # Handle button press events
            # X = 0
            # Square = 2
            # Triangle = 3
            # Circle = 1
            # Up = 11
            # Down = 12
            # Left = 13
            # Right = 14
            # L1 = 9
            # R1 = 10
            # L3 = 7   
            # R3 = 8
            # Start = 6
            # Select = 4
            # Touchpad press = 15
            # L2 = Axis 4
            # R2 = Axis 5
            elif event.type == pygame.JOYBUTTONDOWN:
                if l2_press:
                    if event.button == 0: # X with L2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('x')
                    if event.button == 2: # Square with L2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('c')
                    if event.button == 3: # Triangle with L2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('v')
                    if event.button == 1: # Circle with L2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('d')
                elif r2_press:
                    print(r2_press)
                else:
                    if event.button == 0:  # X button
                        mouse.press(Button.left)  # Left mouse button down
                    if event.button == 1:  # Circle button
                        keyboard.press(Key.backspace)
                    if event.button == 2:  # Square button
                        keyboard.press(Key.space)
                    if event.button == 3:  # Triangle button
                        keyboard.press(Key.shift)
                        keyboard.press(Key.tab)
                    if event.button == 8: # R3
                        mouse.press(Button.right) 
                    if event.button == 11: # Up arrow
                        keyboard.press(Key.up)
                    if event.button == 12: # Down arrow
                        keyboard.press(Key.down)
                    if event.button == 13: # Left arrow
                        keyboard.press(Key.left)
                    if event.button == 14: # Right arrow
                        keyboard.press(Key.right)
                    if event.button == 6: # Start
                        keyboard.press(Key.ctrl)
                        keyboard.press('s')
            elif event.type == pygame.JOYBUTTONUP:     
                if l2_press:
                    if event.button == 0: # X with L2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('x')
                    if event.button == 2: # Square with L2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('c')
                    if event.button == 3: # Triangle with L2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('v')
                    if event.button == 1: # Circle with L2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('d')
                elif r2_press:
                    print(r2_press)
                else:
                    if event.button == 0:  # X button      
                        mouse.release(Button.left)  
                    if event.button == 1:  # Circle button
                        keyboard.release(Key.backspace) 
                    if event.button == 2:  # Square button
                        keyboard.release(Key.space) 
                    if event.button == 3:  # Triangle button
                        keyboard.release(Key.shift)
                        keyboard.release(Key.tab)
                    if event.button == 8: # R3
                        mouse.release(Button.right) # Release right mouse button
                    if event.button == 11: # Up arrow
                        keyboard.release(Key.up)
                    if event.button == 12: # Down arrow
                        keyboard.release(Key.down)
                    if event.button == 13: # Left arrow
                        keyboard.release(Key.left)
                    if event.button == 14: # Right arrow
                        keyboard.release(Key.right)
                    if event.button == 6: # Start
                        keyboard.release(Key.ctrl)
                        keyboard.release('s')
                


        # Move the mouse by the calculated velocity
        if abs(x_velocity) > 0.01 or abs(y_velocity) > 0.01:  # Small threshold to prevent drift
            mouse.move(x_velocity, y_velocity)
        
        # Minimal delay to avoid excessive CPU usage
        time.sleep(0.001)

except KeyboardInterrupt:
    print("Exiting...")

# Quit pygame
pygame.quit()
