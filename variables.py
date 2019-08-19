#!/bin/python3

# Game variables that can be changed!

# game background colour.
BACKGROUND_COLOUR = 'white'

# map variables.
MAX_TILES = 25
MAP_WIDTH = 15
MAP_HEIGHT = 15

# variables representing the different resources.
DIRT = 0
GRASS = 1
WATER = 2
BRICK = 3
WOOD = 4
SAND = 5
PLANK = 6
GLASS = 7

# a list of all game resources.
resources = [DIRT, GRASS, WATER, BRICK, WOOD, SAND, PLANK, GLASS]

# the names of the resources.
names = {
    DIRT: 'dirt',
    GRASS: 'grass',
    WATER: 'water',
    BRICK: 'brick',
    WOOD: 'wood',
    SAND: 'sand',
    PLANK: 'plank',
    GLASS: 'glass'
}

# a dictionary linking resources to images.
textures = {
    DIRT: 'images/dirt.png',
    GRASS: 'images/grass.png',
    WATER: 'images/water.png',
    BRICK: 'images/brick.png',
    WOOD: 'images/wood.png',
    SAND: 'images/sand.png',
    PLANK: 'images/plank.png',
    GLASS: 'images/glass.png'
}

# the number of each resource the player has.
inventory = {
    DIRT: 10,
    GRASS: 10,
    WATER: 10,
    BRICK: 0,
    WOOD: 5,
    SAND: 5,
    PLANK: 0,
    GLASS: 0
}

# the player image.
player_img = 'images/player.png'

# the player position.
player_x = 0
player_y = 0

# rules to make new resources.
crafting = {
    BRICK: {WATER: 1, DIRT: 2},
    PLANK: {WOOD: 3},
    GLASS: {SAND: 3}
}

# keys for placing resources.
place_keys = {
    DIRT: '1',
    GRASS: '2',
    WATER: '3',
    BRICK: '4',
    WOOD: '5',
    SAND: '6',
    PLANK: '7',
    GLASS: '8'
}

# keys for crafting tiles.
craft_keys = {
    BRICK: 'r',
    PLANK: 'u',
    GLASS: 'p'
}

# game instructions that are displayed.
instructions = [
    'Instructions:',
    'Use WASD to move'
]
