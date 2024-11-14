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
sensitivity = 5.0  # Adjust for base speed
deadzone = 0.05  # Ignore small movements
smoothing_factor = 0.1  # Lower for faster response

# Sensitivity for scrolling
scroll_sensitivity = 1.5  # Adjust this for faster/slower scrolling

# Set up a clock to manage refresh rate
clock = pygame.time.Clock()
refresh_rate = 120

# Threshold for L2 and R2 press
trigger_threshold = 0.5  # Move this outside the loop for better readability

# Initialize position deltas for smooth movement
x_velocity = 0
y_velocity = 0
previous_x_move = 0
previous_y_move = 0
previous_x_scroll = 0
previous_y_scroll = 0
right_stick_x_velocity = 0
right_stick_y_velocity = 0
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
        # Update the Pygame event queue to keep joystick data fresh
        pygame.event.pump()
        clock.tick(refresh_rate)
        # Poll events
        for event in pygame.event.get():
            # Handle JOYAXISMOTION for mouse control
            if event.type == pygame.JOYAXISMOTION:
                # Read the X and Y axis (usually axis 0 and 1 for left stick)
                x_axis = controller.get_axis(0)  # Left stick X-axis
                y_axis = controller.get_axis(1)  # Left stick Y-axis
                
                # Move the mouse
                if abs(x_axis) > 0.1 or abs(y_axis > 0.1):  # Add a deadzone for better control
                    # Smooth the movement by interpolating between previous and current values
                    smooth_x_move = (1 - smoothing_factor) * previous_x_move + (smoothing_factor * x_axis)
                    smooth_y_move = (1 - smoothing_factor) * previous_y_move + (smoothing_factor * y_axis)

                    # Scale joystick values to mouse movement
                    # Joystick values are between -1 and 1; multiply by sensitivity
                    x_movement = int(x_axis * sensitivity)
                    y_movement = int(y_axis * sensitivity)

                    # Move the mouse
                    mouse.move(x_movement, y_movement)  
                    
                    # Update previous positions for the next smoothing calculation
                    previous_x_move = smooth_x_move
                    previous_y_move = smooth_y_move

                # Scrolling with Right Stick
                # Right stick axes for scrolling
                x_scroll = controller.get_axis(2)  # Right stick X-axis
                y_scroll = controller.get_axis(3)  # Right stick Y-axis

                # Vertical scrolling
                if abs(y_scroll) > 0.1:  # Add a deadzone for better control
                    smooth_y_scroll = (1 - smoothing_factor) * previous_y_scroll + (smoothing_factor * y_scroll)
                    scroll_amount = int(smooth_y_scroll * scroll_sensitivity)
                    mouse.scroll(0, -scroll_amount)
                    previous_y_scroll = smooth_y_scroll
                
                # Horizontal scrolling
                if abs(x_scroll) > 0.1:  # Add a deadzone for better control
                    smooth_x_scroll = (1 - smoothing_factor) * previous_x_scroll + (smoothing_factor * x_scroll)
                    scroll_amount = int(smooth_x_scroll * scroll_sensitivity)
                    mouse.scroll(-scroll_amount, 0)
                    previous_x_scroll = smooth_x_scroll

                # Handle L2 and R2 (Triggers as buttons)
                if event.axis == 4:  # L2
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
                    if event.button == 0: # X with R2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('e')
                    if event.button == 2: # Square with R2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('g')
                    if event.button == 3: # Triangle with R2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press(Key.shift)
                        keyboard.press('g')
                    if event.button == 1: # Circle with R2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('j')
                    if event.button == 11: # Up with R2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('a')
                    if event.button == 12: # Down with R2 pressed
                        keyboard.press('0')
                    if event.button == 13: # Left with R2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('z')
                    if event.button == 14: # Right with R2 pressed
                        keyboard.press(Key.ctrl)
                        keyboard.press('y')
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
                    if event.button == 9: # L1
                        keyboard.press(Key.shift)
                    if event.button == 10: # R1
                        keyboard.press(Key.enter)
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
                    if event.button == 0: # X with R2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('e')
                    if event.button == 2: # Square with R2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('g')
                    if event.button == 3: # Triangle with R2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release(Key.shift)
                        keyboard.release('g')
                    if event.button == 1: # Circle with R2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('j')
                    if event.button == 11: # Up with R2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('a')
                    if event.button == 12: # Down with R2 pressed
                        keyboard.release('0')
                    if event.button == 13: # Left with R2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('z')
                    if event.button == 14: # Right with R2 pressed
                        keyboard.release(Key.ctrl)
                        keyboard.release('y')
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
                    if event.button == 9: # L1
                        keyboard.release(Key.shift)
                    if event.button == 10: # R1
                        keyboard.release(Key.enter)
                
        # Minimal delay to avoid excessive CPU usage
        time.sleep(0.001)

except KeyboardInterrupt:
    print("Exiting...")

# Quit pygame
pygame.quit()
