from operator import le
import pygame
from game.tiles import Tile
from res.levels import tile_size

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift_x = 0
        self.world_shift_y = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()  #Group of tiles that form the level
        self.player = pygame.sprite.GroupSingle() #Group to represent the player
        
        #Iterate through the level layout in order to build it
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                #Check to see if we have to add a wall tile
                if cell == 'X':
                    tile = Tile((x, y), tile_size, 'gray')
                    self.tiles.add(tile)
                
                #Check to see if we have to add a player tile
                if cell == 'P':
                    tile = Tile((x, y), tile_size, 'red')
                    self.tiles.add(tile)

    def run(self):
        #Update method that allows us to move through the map based on the player inputs
        #self.tiles.update(self.world_shift_x, self.world_shift_y)

        self.tiles.draw(self.display_surface) #Draw the level itself
        self.player.draw(self.display_surface) #Draw the player