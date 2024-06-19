from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random  # Import du module random

app = Ursina()

# Chargement des textures
grass_texture = load_texture('assest/grass.png')
stone_texture = load_texture('assest/stone.png')
wood_texture = load_texture('assest/wood.png')
leaves_texture = load_texture('assest/leaves.png')
sky_texture = load_texture('assest/sky.png')

# Chargement des sons
break_song = Audio('assest/break.mp3', autoplay=False)
place_song = Audio('assest/place.mp3', autoplay=False)

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture='white'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=1
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                voxel = Voxel(position=self.position + mouse.normal, texture=grass_texture)
                place_song.play()  # Jouer le son de placement
            elif key == 'left mouse down':
                destroy(self)
                break_song.play()  # Jouer le son de cassage

def create_tree(position):
    # Tronc de l'arbre
    for i in range(4):
        voxel = Voxel(position=(position[0], position[1] + i, position[2]), texture=wood_texture)
    
    # Feuillage de l'arbre
    for x in range(-1, 2):
        for z in range(-1, 2):
            for y in range(3, 5):
                if x == 0 and z == 0 and y == 4:  # éviter les collisions avec le tronc
                    continue
                voxel = Voxel(position=(position[0] + x, position[1] + y, position[2] + z), texture=leaves_texture)

# Génération d'une carte plus grande
for z in range(32):  # Augmenter la taille de la carte
    for x in range(32):  # Augmenter la taille de la carte
        if random.random() < 0.1:  # Probabilité de 10% d'avoir un bloc de pierre
            voxel = Voxel(position=(x, 0, z), texture=stone_texture)
        else:
            voxel = Voxel(position=(x, 0, z), texture=grass_texture)

# Ajout d'arbres à des positions spécifiques
create_tree((5, 1, 5))
create_tree((10, 1, 10))
create_tree((15, 1, 15))

player = FirstPersonController()

# Ajout de la texture du ciel
sky = Sky(texture=sky_texture)

app.run()
