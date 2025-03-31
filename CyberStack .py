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
        box = Button(color=color.white, model='cube', position=(j, 0, i),
                     texture='grass.png', parent=scene, origin_y=0.5)
        boxes.append(box)

# Store placed blocks in a list
blocks = []

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

# Run the Ursina app
app.run()