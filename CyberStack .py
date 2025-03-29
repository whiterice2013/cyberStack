from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Initialize the Ursina app
app = Ursina()

# Create a player with first-person controls
player = FirstPersonController()

# Set up the sky
Sky()

# Store blocks in a list to track them
boxes = []

# Create the ground with a simple 20x20 grid of blocks
for i in range(20):
    for j in range(20):
        box = Button(color=color.white, model='cube', position=(j, 0, i),
                     texture='grass.png', parent=scene, origin_y=0.5)
        boxes.append(box)

# Gravity settings
g = 1  # gravitational acceleration
y_velocity = 0  # Initial vertical velocity (0 means no movement)

# Time counter for gravity simulation
falling = True  # True when player is falling, False when jumping

# Function to handle block placement and removal
def input(key):
    for box in boxes:
        if box.hovered:
            if key == 'right mouse down':  # Place a block in the direction of the mouse
                new = Button(color=color.white, model='cube', position=box.position + mouse.normal,
                             texture='grass.png', parent=scene, origin_y=0.5)
                boxes.append(new)

            if key == 'left mouse down':  # Destroy the block that is hovered over
                boxes.remove(box)
                destroy(box)

# Function to update the game mechanics (like gravity, jumping, and movement)
def update():
    global y_velocity, falling

    # Gravity effect (falling down)
    if player.y > 0:  # The player is falling (y > 0)
        y_velocity += g  # Increase downward speed each frame

    if player.y <= 0:  # When player hits the ground
        player.y = 0
        y_velocity = 0  # Reset velocity to 0 (no downward speed)
        falling = False  # Stop falling once the player touches the ground

    # Apply gravity (moving the player down)
    player.y -= y_velocity  # Decrease the player's y position by the velocity

    # Jumping action
    if not falling and held_keys['space']:  # Jump if on the ground and space is pressed
        y_velocity = -10  # Give the player an upward velocity to simulate jumping
        falling = True  # Start the falling effect after jumping

    # Add additional mechanics like crouching, sprinting, etc.

# Run the Ursina app
app.run()
