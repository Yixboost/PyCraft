from turtle import position, pu
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
rain_texture = load_texture("regen.gif")
sky_texture = load_texture("Skybox.png")
arm_texture = load_texture("Arm_Texture.png")
punch_sound = Audio("Punch_Sound.wav", loop = False, autoplay = False)
window.exit_button.visible = False
block_pick = 1

# Updates every frame
def update():
    global block_pick

    if held_keys["left mouse"] or held_keys["right mouse"]:
        hand.active()
    else:
        hand.passive()

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

# Increase the numbers for more cubes. For exapmle: for z in range(20)
for z in range(40):
    for x in range(40):
        voxel = Voxel(position = (x, 0, z))

for z in range(40):
    for x in range(40):
        voxel = Voxel(position = (x, 1, z))

for z in range(40):
    for x in range(40):
        voxel = Voxel(position = (x, 2, z))


player = FirstPersonController()
sky = Sky()
hand = Hand()


app.run()
