
import pygame
import numpy as np
from map.tiles import Tile
from res.levels import *
from utils.observer import Observer

class Level(Observer):
    def __init__(self, level_data):
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.levels = np.zeros((room_num), dtype=bool)

        self.setup_level(level_data)

    def __addRoom(self, room, layout_door_pos, orientation):
        row_index = layout_door_pos[0]
        col = layout_door_pos[1]

        #Get the door position in the room
        for room_row_index, room_row in enumerate(room):
            for room_col_index, room_cell in enumerate(room_row):
                if room_cell == 'D':
                    r = room_row_index
                    c = room_col_index

        #Calculating starting point to add the room on the basic layout
        if orientation:
            start_row = row_index + r
            start_col = col + c
        else:
            start_row = row_index - r
            start_col = col - c

        #Iterate to add each cell
        for room_row_index, room_row in enumerate(room):
            aux_x = start_col
            for room_col_index, room_cell in enumerate(room_row):
                #Check to see if there is a wall on the room layout
                if room_cell == 'X':

                    if aux_x == 0:
                        x = aux_x + tile_size
                    else:
                        x = aux_x * tile_size

                    if start_row == 0:
                        y = start_row + tile_size
                    else:
                        y = start_row * tile_size

                    #Adding the tile to the tile group
                    tile = Tile((x, y), tile_size, 'white')
                    self.tiles.add(tile)

                if orientation:
                    aux_x -= 1
                else: 
                    aux_x += 1

            if orientation:
                start_row -= 1
            else: 
                start_row += 1

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()  #Group of tiles that form the map
        self.player = pygame.sprite.GroupSingle() #Group to represent the player
        inside = False
        
        #Iterate through the map layout in order to build it
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                #Check to see if we have to add a wall tile
                if cell == 'X':
                    inside = not inside #Complement of current value

                    tile = Tile((x, y), tile_size, 'gray')
                    self.tiles.add(tile)
                
                #Check to see if we have to add a player tile
                if cell == 'P':
                    tile = Tile((x, y), tile_size, 'red')
                    self.tiles.add(tile)
                
                #Check to see if we have a door
                if cell == 'D':

                    #Get the room we want to add
                    while True:
                        num = np.random.randint(0, room_num)
                        if self.levels[num] == False:
                            self.levels[num] = True
                            break

                    #Get the room from the list of rooms based on the random number
                    room = rooms[num]

                    if inside:
                        
                        #The empty space on the map is to the right of the door
                        col = col_index + 1

                        #Add the room
                        self.__addRoom(room, (row_index, col), inside)
                        
                    else:

                        #The empty space on the map is to the left of the door
                        col = col_index - 1

                        #Add the room
                        self.__addRoom(room, (row_index, col), inside)
                
                    inside = not inside  # Complement of current value

                    


    def run(self, surface):
        #Update method that allows us to move through the map based on the player inputs
        self.tiles.update(self.world_shift_x, self.world_shift_y)

        self.display_surface = surface;

        if self.display_surface is None:
            print("ERROR: No display surface to draw on.")
            exit(-1)
        else:    
            self.tiles.draw(self.display_surface) #Draw the map itself
            self.player.draw(self.display_surface) #Draw the player