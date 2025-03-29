from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Initialize the Ursina app
app = Ursina()

# Create a player with first-person controls
player = FirstPersonController()

# Set up the sky
Sky()

# Store blocks in a list
boxes = []

# Create a 20x20 ground
for i in range(20):
    for j in range(20):
        box = Button(color=color.white, model='cube', position=(j, 0, i),
                     texture='grass.png', parent=scene, origin_y=0.5)
        boxes.append(box)

# Function to handle block placement and removal
def input(key):
    for box in boxes:
        if box.hovered:
            if key == 'right mouse down':  # Place a block
                new = Button(color=color.white, model='cube', position=box.position + mouse.normal,
                             texture='grass.png', parent=scene, origin_y=0.5)
                boxes.append(new)

            if key == 'left mouse down':  # Destroy a block
                boxes.remove(box)
                destroy(box)

# Physics settings
gravity = 0.3  # How fast the player falls
jump_strength = 7  # Initial jump speed
y_velocity = 0  # Player's vertical velocity
can_jump = True  # Prevent multiple jumps

def is_on_ground():
    """ Check if there's a block under the player """
    hit_info = raycast(player.position, direction=(0, -1, 0), distance=1.1, ignore=[player]) 
    return hit_info.hit  # Returns True if standing on a block

def update():
    global y_velocity, can_jump

    # Apply gravity
    if not is_on_ground():
        y_velocity -= gravity  # Gravity slows down the jump and makes falling smooth
        player.y += y_velocity
    else:
        y_velocity = 0  # Stop falling when on a block
        can_jump = True  # Reset jump ability

        # Jumping (now with a single press)
        if held_keys['space'] and can_jump:
            can_jump = False  # Disable jumping until the player lands
            y_velocity = jump_strength  # Give an initial strong push upwards
            player.y += y_velocity

    # Prevent player from falling too far
    if player.y < -10:
        player.position = (0, 5, 0)  # Reset to a safe position

# Run the Ursina app
app.run()
