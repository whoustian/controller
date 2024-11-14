import pygame
from pynput.mouse import Controller

# Initialize Pygame and the joystick
pygame.init()
pygame.joystick.init()

# Initialize the mouse controller
mouse = Controller()

# Set up the joystick (assuming there's only one connected)
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Sensitivity factor for mouse movement (adjust as necessary)
sensitivity = 5.0

print("Starting joystick control of the mouse. Press CTRL+C to quit.")

try:
    while True:
        # Process Pygame events
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                # Read the X and Y axis (usually axis 0 and 1 for left stick)
                x_axis = joystick.get_axis(0)  # Left stick X-axis
                y_axis = joystick.get_axis(1)  # Left stick Y-axis
                
                # Scale joystick values to mouse movement
                # Joystick values are between -1 and 1; multiply by sensitivity
                x_movement = int(x_axis * sensitivity)
                y_movement = int(y_axis * sensitivity)
                
                # Move the mouse
                mouse.move(x_movement, y_movement)
except KeyboardInterrupt:
    print("\nJoystick control ended.")

finally:
    # Clean up Pygame
    pygame.quit()
