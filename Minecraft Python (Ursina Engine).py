from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Variables
creeper_texture = load_texture("Creeper_Block.png")
steve_texture = load_texture("Steve_Block.png")
steen_texture = load_texture("Steen_Block.png")
gold_texture = load_texture("Gold_Block.png")
lava_texture = load_texture("Lava_Block.png")
grass_texture = load_texture("Grass_Block.png")
stone_texture = load_texture("Stone_Block.png")
brick_texture = load_texture("Brick_Block.png")
dirt_texture = load_texture("Dirt_Block.png")
wood_texture = load_texture("Wood_Block.png")
poke_texture = load_texture("Pokeball_Block.png")
rain_texture = load_texture("regen.gif")
sky_texture = load_texture("Skybox.png")
arm_texture = load_texture("Arm_Texture.png")
punch_sound = Audio("Punch_Sound.wav", loop=False, autoplay=False)
window.exit_button.visible = False
block_pick = 1

# Block selector GUI
class BlockSelector(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.bg = Entity(
            parent=self,
            model='quad',
            scale=(0.6, 0.8),
            color=color.color(0, 0, 0, 0.8),
            position=(0, 0),
            enabled=False
        )
        
        # Dictionary mapping block IDs to their textures and names
        self.blocks = {
            1: {'texture': grass_texture, 'name': 'Grass'},
            2: {'texture': stone_texture, 'name': 'Stone'},
            3: {'texture': brick_texture, 'name': 'Brick'},
            4: {'texture': dirt_texture, 'name': 'Dirt'},
            5: {'texture': wood_texture, 'name': 'Wood'},
            6: {'texture': gold_texture, 'name': 'Gold'},
            7: {'texture': lava_texture, 'name': 'Lava'},
            8: {'texture': steen_texture, 'name': 'Steen'},
            9: {'texture': steve_texture, 'name': 'Steve'},
            0: {'texture': creeper_texture, 'name': 'Creeper'}
        }
        
        # Create block buttons
        self.buttons = []
        x_start = -0.25
        y_start = 0.3
        spacing = 0.1
        
        for i, (block_id, block_info) in enumerate(self.blocks.items()):
            x = x_start + (i % 5) * spacing
            y = y_start - (i // 5) * spacing
            
            button = Button(
                parent=self.bg,
                model='quad',
                texture=block_info['texture'],
                scale=0.08,
                position=(x, y),
                color=color.white,
                highlight_color=color.light_gray,
                pressed_color=color.gray
            )
            
            # Add text label below button
            text = Text(
                parent=self.bg,
                text=f"{block_info['name']}\n({block_id})",
                scale=1.5,
                position=(x, y-0.05),
                origin=(0, 0),
                color=color.white
            )
            
            # Store block_id in the button for easy access
            button.block_id = block_id
            button.on_click = self.select_block
            self.buttons.append(button)
        
        self.visible = False
    
    def select_block(self):
        global block_pick
        block_pick = self.buttons[self.buttons.index(mouse.hovered_entity)].block_id
        self.toggle()
    
    def toggle(self):
        self.bg.enabled = not self.bg.enabled
        if self.bg.enabled:
            mouse.locked = False
        else:
            mouse.locked = True

# Updates every frame
def update():
    global block_pick
    
    if held_keys["left mouse"] or held_keys["right mouse"]:
        hand.active()
    else:
        hand.passive()
    
    # Number key shortcuts still work
    if held_keys["1"]: block_pick = 1
    if held_keys["2"]: block_pick = 2
    if held_keys["3"]: block_pick = 3
    if held_keys["4"]: block_pick = 4
    if held_keys["5"]: block_pick = 5
    if held_keys["6"]: block_pick = 6
    if held_keys["7"]: block_pick = 7
    if held_keys["8"]: block_pick = 8
    if held_keys["9"]: block_pick = 9
    if held_keys["0"]: block_pick = 0

def input(key):
    if key == 'b':
        block_selector.toggle()



# Voxel (block) properties
class Voxel(Button):
    def __init__(self, position = (0, 0, 0), texture = grass_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = "Block",
            origin_y = 1,
            texture = texture,
            color = color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color = color.light_gray,
            scale = 0.5
        )



    # What happens to blocks on inputs
    def input(self,key):
        if self.hovered:
            if key == "left mouse down":
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
                if block_pick == 5: voxel = Voxel(position = self.position + mouse.normal, texture = wood_texture)
                if block_pick == 6: voxel = Voxel(position = self.position + mouse.normal, texture = gold_texture)
                if block_pick == 7: voxel = Voxel(position = self.position + mouse.normal, texture = lava_texture)
                if block_pick == 8: voxel = Voxel(position = self.position + mouse.normal, texture = steen_texture)
                if block_pick == 9: voxel = Voxel(position = self.position + mouse.normal, texture = steve_texture)
                if block_pick == 0: voxel = Voxel(position = self.position + mouse.normal, texture = creeper_texture)
            
            if key == "right mouse down":
                punch_sound.play()
                destroy(self)

# Skybox
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "Sphere",
            texture = sky_texture,
            scale = 150,
            double_sided = True
        )

# Arm
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = "Arm",
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6)
        )
    
    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

# Initialize the world
for z in range(40):
    for x in range(40):
        voxel = Voxel(position=(x, 0, z))

for z in range(40):
    for x in range(40):
        voxel = Voxel(position=(x, 1, z))

for z in range(40):
    for x in range(40):
        voxel = Voxel(position=(x, 2, z))

player = FirstPersonController()
sky = Sky()
hand = Hand()
block_selector = BlockSelector()

app.run()
