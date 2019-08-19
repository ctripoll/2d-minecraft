# import the modules and variables needed
import turtle
import random
from variables import *
from math import ceil


#############
# CodeCraft #
#############

# ---
# Game functions
# ---

# moves the player left 1 tile.
def move_left():
    global player_x
    if player_x > 0:
        player_x -= 1
        draw_player()


# moves the player right 1 tile.
def move_right():
    global MAP_WIDTH, player_x
    if player_x < MAP_WIDTH - 1:
        player_x += 1
        draw_player()


# moves the player up 1 tile.
def move_up():
    global player_y
    if player_y > 0:
        player_y -= 1
        draw_player()


# moves the player down 1 tile.
def move_down():
    global player_y, MAP_HEIGHT
    if player_y < MAP_HEIGHT - 1:
        player_y += 1
        draw_player()


# picks up the resource at the player's position.
def pick_up():
    global player_x, player_y
    drawing = True
    current_tile = world[player_x][player_y]
    # if the user doesn't already have too many...
    if inventory[current_tile] < MAX_TILES:
        # player now has 1 more of this resource
        inventory[current_tile] += 1
        # the player is now standing on dirt
        world[player_x][player_y] = DIRT
        # draw the new DIRT tile
        draw_resource(player_x, player_y)
        # redraw the inventory with the extra resource.
        draw_inventory()


# place a resource at the player's current position
def place(resource):
    print('placing: ', names[resource])
    # only place if the player has some left...
    if inventory[resource] > 0:
        # find out the resource at the player's current position
        current_tile = world[player_x][player_y]
        # pick up the resource the player's standing on
        # (if it's not DIRT)
        if current_tile is not DIRT:
            inventory[current_tile] += 1
        # place the resource at the player's current position
        world[player_x][player_y] = resource
        # add the new resource to the inventory
        inventory[resource] -= 1
        # update the display (world and inventory)
        draw_resource(player_x, player_y)
        draw_inventory()
        print('   Placing', names[resource], 'complete')
    # ...and if they have none left...
    else:
        print('   You have no', names[resource], 'left')


# craft a new resource
def craft(resource):
    print('Crafting: ', names[resource])
    # if the resource can be crafted...
    if resource in crafting:
        # keeps track of whether we have the resources
        # to craft this item
        can_be_made = True
        # for each item needed to craft the resource
        for i in crafting[resource]:
            # ...if we don't have enough...
            if crafting[resource][i] > inventory[i]:
                # ...we can't craft it!
                can_be_made = False
                break
        # if we can craft it (we have all needed resources)
        if can_be_made:
            # take each item from the inventory
            for i in crafting[resource]:
                inventory[i] -= crafting[resource][i]
            # add the crafted item to the inventory
            inventory[resource] += 1
            print('   Crafting', names[resource], 'complete')
        # ...otherwise the resource can't be crafted...
        else:
            print('   Can\'t craft', names[resource])
        # update the displayed inventory
        draw_inventory()


# creates a function for placing each resource
def make_place(resource):
    return lambda: place(resource)


# attaches a 'placing' function to each key press
def bind_placing_keys():
    for k in place_keys:
        screen.onkey(make_place(k), place_keys[k])


# creates a function for crafting each resource
def make_craft(resource):
    return lambda: craft(resource)


# attaches a 'crafting' function to each key press
def bind_crafting_keys():
    for k in craft_keys:
        screen.onkey(make_craft(k), craft_keys[k])


# draws a resource at the position (y,x)
def draw_resource(y, x):
    # this variable stops other stuff being drawn
    global drawing
    # only draw if nothing else is being drawn
    if not drawing:
        # something is now being drawn
        drawing = True
        # draw the resource at that position in the tilemap, using the correct image
        rendererT.goto((y * TILE_SIZE) + 20, height - (x * TILE_SIZE) - 20)
        # draw tile with correct texture
        tex = textures[world[y][x]]
        rendererT.shape(tex)
        rendererT.stamp()
        screen.update()
        # nothing is now being drawn
        drawing = False


# draws the player on the world
def draw_player():
    playerT.goto((player_x * TILE_SIZE) + 20, height - (player_y * TILE_SIZE) - 20)


# draws the world map
def draw_world():
    # loop through each row
    for row in range(MAP_HEIGHT):
        # loop through each column in the row
        for column in range(MAP_WIDTH):
            # draw the tile at the current position
            draw_resource(column, row)


# draws the inventory to the screen
def draw_inventory():
    # this variable stops other stuff being drawn
    global drawing
    # only draw if nothing else is being drawn
    if not drawing:
        # something is now being drawn
        drawing = True
        # use a rectangle to cover the current inventory
        rendererT.color(BACKGROUND_COLOUR)
        rendererT.goto(0, 0)
        rendererT.begin_fill()
        # rendererT.setheading(0)
        for i in range(2):
            rendererT.forward(inventory_height - 60)
            rendererT.right(90)
            rendererT.forward(width)
            rendererT.right(90)
        rendererT.end_fill()
        rendererT.color('')
        # display the 'place' and 'craft' text
        for i in range(1, num_rows + 1):
            rendererT.goto(20, (height - (MAP_HEIGHT * TILE_SIZE)) - 20 - (i * 100))
            rendererT.write("place")
            rendererT.goto(20, (height - (MAP_HEIGHT * TILE_SIZE)) - 40 - (i * 100))
            rendererT.write("craft")
        # set the inventory position
        x_position = 70
        y_position = height - (MAP_HEIGHT * TILE_SIZE) - 80
        item_num = 0
        for i, item in enumerate(resources):
            # add the image
            rendererT.goto(x_position, y_position)
            rendererT.shape(textures[item])
            rendererT.stamp()
            # add the number in the inventory
            rendererT.goto(x_position, y_position - TILE_SIZE)
            rendererT.write(inventory[item])
            # add key to place
            rendererT.goto(x_position, y_position - TILE_SIZE - 20)
            rendererT.write(place_keys[item])
            # add key to craft
            if crafting.get(item) is not None:
                rendererT.goto(x_position, y_position - TILE_SIZE - 40)
                rendererT.write(craft_keys[item])
                # move along to place the next inventory item
            x_position += 50
            item_num += 1
            # drop down to the next row every 10 items
            if item_num % INV_WIDTH == 0:
                x_position = 70
                item_num = 0
                y_position -= TILE_SIZE + 80
        drawing = False


# generate the instructions, including crafting rules
def generate_instructions():
    instructions.append('Crafting rules:')
    # for each resource that can be crafted...
    for rule in crafting:
        # create the crafting rule text
        craft_rule = names[rule] + ' = '
        for resource, number in crafting[rule].items():
            craft_rule += str(number) + ' ' + names[resource] + ' '
        # add the crafting rule to the instructions
        instructions.append(craft_rule)
    # display the instructions
    y_pos = height - 20
    for item in instructions:
        rendererT.goto(MAP_WIDTH * TILE_SIZE + 40, y_pos)
        rendererT.write(item)
        y_pos -= 20


# generate a random world
def generate_random_world():
    # loop through each row
    for row in range(MAP_HEIGHT):
        # loop through each column in that row
        for column in range(MAP_WIDTH):
            # pick a random number between 0 and 10
            random_number = random.randint(0, 10)
            # WATER if the random number is a 1 or a 2
            if random_number in [1, 2]:
                tile = WATER
            # GRASS if the random number is a 3 or a 4
            elif random_number in [3, 4]:
                tile = GRASS
            # WOOD if it's a 5
            elif random_number == 5:
                tile = WOOD
            # SAND if it's a 6
            elif random_number == 6:
                tile = SAND
            # otherwise it's DIRT
            else:
                tile = DIRT
            # set the position in the tile map to the randomly chosen tile
            world[column][row] = tile


# ---
# Code starts running here
# ---


TILE_SIZE = 20
# the number of inventory resources per row
INV_WIDTH = 8
drawing = False

# create a new 'screen' object
screen = turtle.Screen()
# calculate the width and height
width = (TILE_SIZE * MAP_WIDTH) + max(200, INV_WIDTH * 50)
num_rows = int(ceil((len(resources) / INV_WIDTH)))
inventory_height = num_rows * 120 + 40
height = (TILE_SIZE * MAP_HEIGHT) + inventory_height

screen.setup(width, height)
screen.setworldcoordinates(0, 0, width, height)
screen.bgcolor(BACKGROUND_COLOUR)
screen.listen()

# register the player image
screen.register_shape(player_img)
# register each of the resource images
for texture in textures.values():
    screen.register_shape(texture)

# create a new player object
playerT = turtle.Turtle()
playerT.hideturtle()
playerT.shape(player_img)
playerT.penup()
playerT.speed(0)

# create another turtle to do the graphics drawing
rendererT = turtle.Turtle()
rendererT.hideturtle()
rendererT.penup()
rendererT.speed(0)
rendererT.setheading(90)

# create a world of random resources.
world = [[DIRT for w in range(MAP_HEIGHT)] for h in range(MAP_WIDTH)]

# map the keys for moving and picking up to the correct functions.
screen.onkey(move_up, 'w')
screen.onkey(move_down, 's')
screen.onkey(move_left, 'a')
screen.onkey(move_right, 'd')
screen.onkey(pick_up, 'space')

# set up the keys for placing and crafting each resource
bind_placing_keys()
bind_crafting_keys()

# these functions are defined above
generate_random_world()
draw_world()
draw_inventory()
generate_instructions()
draw_player()
playerT.showturtle()
