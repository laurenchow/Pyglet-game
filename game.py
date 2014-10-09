import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player): 
        player.inventory.append(self)
        if self.SOLID == False:
            GAME_BOARD.draw_msg("You are at a door! You unlocked it!")
 
class Troll(GameElement):
    IMAGE = "Bug"
    SOLID = True
    direction =1

    def update(self, dt):

        next_x = self.x + self.direction

        if next_x < 0 or next_x >= self.board.width:
            self.direction *= -1
            next_x = self.x

        self.board.del_el(self.x, self.y)
        self.board.set_el(next_x, self.y, self)

      
class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" %(len(player.inventory)))

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self,player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired the key! It unlocks things! But what things?")
        Door.SOLID = False

class Character(GameElement):
    IMAGE = "Girl"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def keyboard_handler(self, symbol, modifier):

        direction = None
        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.LEFT:
            direction = "left"
        elif symbol == key.RIGHT:
            direction = "right"

        self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))

        if direction:
            next_location = self.next_pos(direction)
            print "next_location", next_location[0]

            if next_location[0] < 0 or next_location[0] >= self.board.width:
                self.board.draw_msg("You cannot go there! Nice try.")
                next_location = (self.x, self.y)
            
            if next_location[1] < 0 or next_location[1] >= self.board.height:
                self.board.draw_msg("You cannot go there! Nice try.")
                next_location = (self.x, self.y)
                            
            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                existing_el = self.board.get_el(next_x, next_y)

                if existing_el: 
                    existing_el.interact(self)

                if existing_el and existing_el.SOLID: 
                    self.board.draw_msg("There's something in my way!")
                elif existing_el is None or not existing_el.SOLID:    
                    self.board.del_el(self.x, self.y)
                    self.board.set_el(next_x, next_y, self)

    def next_pos(self, direction):
        print "This is the type that we're looking for:"            
        #print type(self.x), type(self.y-1)
        if direction == "up": 
            return (self.x, self.y-1) 
        elif direction == "down": 
            return (self.x, self.y +1)
        elif direction == "left": 
            return(self.x -1, self.y)
        elif direction == "right":
            return (self.x +1, self.y)
        return None
####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
 
    rock_positions = [
            (2, 1),
            (1, 2),
            (3, 2),
            (2, 3),
            (6, 4),
            (8, 2),
            (2, 5),
            (7, 8), 
        ]

    rocks = []
 
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[3].SOLID = False

    for rock in rocks:
        print rock
   
    # Initialize character
    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2, 2, player)
    print player

    GAME_BOARD.draw_msg("This game is wicked awesome.")
    
    # Initialize gem
    gem_positions = [
            (4, 1),
            (1, 6),
            (5, 2),
            (2, 7),
            (4, 6),
 
        ]

    gems = []
 
    for pos in gem_positions:
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)
        gems.append(gem)

    gems[-1].SOLID = True
    # gem = Gem()
    #GAME_BOARD.register(gem)
    #GAME_BOARD.set_el(3, 1, gem)

    # Initialize door
    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(7, 5, door)
 
    #Initialize key
    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(2, 8, key)


    #Initialize troll
    troll = Troll()
    GAME_BOARD.register(troll)
    GAME_BOARD.set_el(7, 6, troll)
    troll.update(troll)