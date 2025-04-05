from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Initialize the Ursina app
app = Ursina()

# Create a player with first-person controls
player = FirstPersonController()
player.jump_height = 2  # Adjust jump height for more natural motion
player.gravity = 0.8  # Gravity strength

# Set up the sky
Sky()

# Store blocks in a list
boxes = []

# Create a 20x20 ground using optimized Entity creation
for i in range(20):
    for j in range(20):
        box = Entity(
            color=color.white,
            model="cube",
            position=(j, 0, i),
            texture="grass",
            parent=scene,
            origin_y=0.5,
            collider="box",
        )
        boxes.append(box)

# Store placed blocks in a list
blocks = []

# Variable to store the currently hovered block
hovered_block = None


# Function to check if a position is too close to the player (on the x and z axes)
def is_too_close_to_player(position):
    return (
        abs(player.position.x - position.x) < 1
        and abs(player.position.z - position.z) < 1
    )


def input(key):
    global hovered_block

    # Handle block placement and removal
    for box in boxes:
        if box.hovered:
            # Check if we are trying to place a block too close to the player on x and z axes
            if is_too_close_to_player(box.position) and key == "right mouse down":
                continue

            if key == "right mouse down":  # Place a block
                new = Entity(
                    color=color.white,
                    model="cube",
                    position=box.position + mouse.normal,
                    texture="grass",
                    parent=scene,
                    origin_y=0.5,
                    collider="box",
                )
                boxes.append(new)

            if key == "left mouse down":  # Destroy a block (no restriction)
                boxes.remove(box)
                destroy(box)


# Run the Ursina app
app.run()
