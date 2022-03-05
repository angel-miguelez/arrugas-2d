from turtle import pos
import pygame
import numpy as np
from map.tiles import Tile
from res.levels import *
from characters.personaje2 import *
from utils.observer import *
from utils.resourcesmanager import *

_LEFTWALL = 0
_RIGHTWALL = 1
_INTERSECTION_TOPRIGHT = 2
_INTERSECTION_TOPLEFT = 3
_INTERSECTION_BOTTOMLEFT = 4
_INTERSECTION_BOTTOMRIGHT = 5
#This is changed as a test the cords of the coordInterior.txt should be 32 160 32 64
_FRONTWALL = 6
_FLOOR_1 = 7
_FLOOR_2 = 8
_FLOOR_3 = 9
_FLOOR_4 = 10
_FLOOR_5 = 11

class Level(Observer):
    def __init__(self, level_data, posx, posy):
        #Load the image
        self.sheet = ResourcesManager.loadImage("Room_Builder_free_32x32.png", -1)
        self.sheet = self.sheet.convert_alpha()

        #Player spawn coords
        self._playerSpawnX = posx
        self._playerSpawnY = posy
        self._playerPosX = posx
        self._playerPosY = posy

        #Load coordinates
        data = ResourcesManager.loadCoordFile("coordInterior.txt")
        data = data.split()

        #Extracting and organizing all the coordinates for the sprites
        self.sheetCoord = []
        tmp = []

        for n in range(0, len(data)):
            if(((n % 4) == 0) | (n == len(data) - 1)):
                if(n > 0):
                    if(n == len(data) - 1):
                        tmp.append(int(data[n]))

                    self.sheetCoord.append(tmp)
                    tmp = []

            tmp.append(int(data[n]))

        self.worldShiftX = posx
        self.worldShiftY = posy
        self.levels = np.zeros((room_num), dtype=bool)

        #Enemy array for room number 1 the enemies would be located on the 0 position of the array so roomNumber - 1
        self.enemies = []

        self.setupLevel(level_data)

    def __setSprite(self, spriteType, pos, tileGroup):
        #Get coordinates and size for the type of sprite requested
        spriteCoords = self.sheetCoord[spriteType]
        
        #Get the sprite from the sprite sheet
        aux = pygame.Rect(
            spriteCoords[0], spriteCoords[1], spriteCoords[2], spriteCoords[3])
        image = self.sheet.subsurface(aux)

        #Create the tile and add it to the corresponding group
        tile = Tile((pos[0], pos[1]), image)
        tileGroup.add(tile)

    def __calculatePos(self, x, y):
        if x == 0:
            x = x + tile_size
        else:
            x = x * tile_size

        if y == 0:
            y = y + tile_size
        else:
            y = y * tile_size

        return (x, y)

    def __addRoom(self, room, layout_door_pos, orientation):
        row_index = layout_door_pos[0]
        col = layout_door_pos[1]

        enemyGroup = pygame.sprite.Group() #We're generating a group of enemies for each room

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
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FRONTWALL, (x, y), self.walls)
                
                #Check to see if we have to add a floor tile
                if room_cell == 'F':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_2, (x, y), self.floor)
                
                """
                    For the automatic enemy generation we should take into account the orientation
                    that the room is generated in, if originally the enemies were on the top-right corner
                    if the room is generated on the right side of the corridor then the enemy would be on
                    the bottom left corner, so depending on the value of the already calculated orientation
                    variable there should be different behaviours
                    
                    Also we have to create a group only for enemies
                """

                #Check to see if we have to add a Basic0 enemy
                #For now it's adding a random tile
                if room_cell == 'R':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_1, (x, y), self.floor)

                    #Create the enemy and add it to the group of enemies of that room
                    waypoints = [(360, 200), (140, 200)]
                    spawn = [x, y]
                    basic1 = Basic1(spawn, waypoints, 1.5)
                    enemyGroup.add(basic1)

                #Check to see if we have to add a Basic1 enemy
                #For now it's adding a random tile
                if room_cell == 'W':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_3, (x, y), self.floor)

                    #Create the enemy and add it to the group of enemies of that room
                    basic0 = Basic0([x, y])
                    enemyGroup.add(basic0)
                
                #Check to see if we have to add a Basic2 enemy
                #For now it's adding a random tile
                if room_cell == 'M':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)
                    
                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_4, (x, y), self.floor)

                    #Create the enemy and add it to the group of enemies of that room
                    basic2 = Basic2([x, y], self.player, 500)
                    enemyGroup.add(basic2)
                
                #Check to see if we have to add a Basic3 enemy
                #For now it's adding a random tile
                if room_cell == 'T':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)
                    
                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_5, (x, y), self.floor)

                    #Create the enemy and add it to the group of enemies of that room
                    #normal2 = Normal2([x, y], self.player)
                    #enemyGroup.add(normal2)
                
                #Check to see if we have to add a floor tile
                if room_cell == 'D':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_2, (x, y), self.floor)

                if orientation:
                    aux_x -= 1
                else: 
                    aux_x += 1

            if orientation:
                start_row -= 1
            else: 
                start_row += 1

        print(enemyGroup)
        self.enemies.append(enemyGroup)

    def __setupPlayerSpawn(self):
        difference = (self._playerPosX -
                      self._playerSpawnX, self._playerPosY - self._playerSpawnY)

        self.walls.update(difference[0], difference[1])
        self.floor.update(difference[0], difference[1])
        #The player won't be needing this kind of updates later on
        self.player.update(difference[0], difference[1])
        
        #Updating enemies position based on the player spawn
        #for enemyGroup in self.enemies:
        #    enemyGroup.update(difference[0], difference[1])


    def setupLevel(self, layout):
        self.walls = pygame.sprite.Group()  #Group of tiles that form the walls of the map
        self.floor = pygame.sprite.Group()  # Group of tiles that form the floor of the map
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

                    self.__setSprite(_FRONTWALL, (x, y), self.walls)

                #Check to see if we have to add a floor tile
                if cell == 'F':

                    self.__setSprite(_FLOOR_2, (x, y), self.floor)
                
                #Check to see if we have to add a left wall tile
                if cell == 'L':
                    inside = not inside  # Complement of current value

                    self.__setSprite(_FRONTWALL, (x, y), self.walls)
                
                #Check to see if we have to add a right wall tile
                if cell == 'R':
                    inside = not inside  # Complement of current value

                    self.__setSprite(_FRONTWALL, (x, y), self.walls)
                
                #Check to see if we have to add a top right intersection tile
                if cell == 'K':
                    inside = not inside  # Complement of current value

                    self.__setSprite(_FRONTWALL, (x, y), self.walls)
                
                #Check to see if we have to add a top left intersection tile
                if cell == 'J':
                    inside = not inside  # Complement of current value

                    self.__setSprite(_FRONTWALL, (x, y), self.walls)
                
                #Check to see if we have to add a bottom left intersection tile
                if cell == 'H':
                    inside = not inside  # Complement of current value

                    self.__setSprite(_FRONTWALL, (x, y), self.walls)
                
                #Check to see if we have to add a bottom right intersection tile
                if cell == 'G':
                    inside = not inside  # Complement of current value

                    self.__setSprite(_FRONTWALL, (x, y), self.walls)

                #Check to see if we have to add a player tile
                if cell == 'P':
                    #Later on this will draw a floor tile

                    self._playerSpawnX = x
                    self._playerSpawnY = y

                    self.__setSprite(_LEFTWALL, (x, y), self.player)
                
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
                    
                    self.__setSprite(_FLOOR_2, (x, y), self.floor)
            
        self.__setupPlayerSpawn()
        


    def draw(self, surface):
        self.display_surface = surface

        if self.display_surface is None:
            print("ERROR: No display surface to draw on.")
            exit(-1)
        else:    
            self.walls.draw(self.display_surface) #Draw the walls of the map itself
            self.floor.draw(self.display_surface) #Draw the floor of the map itself
            self.player.draw(self.display_surface) #Draw spawn of the player
            for enemyGroup in self.enemies:
                enemyGroup.draw(self.display_surface)  # Draw the enemies
    
    def updateObserver(self, subject: Player):
        newPos = subject.getPos()
        difference = (self.worldShiftX -
                      newPos[0], self.worldShiftY - newPos[1])

        self.worldShiftX = newPos[0]
        self.worldShiftY = newPos[1]

        self.walls.update(difference[0], difference[1])
        self.floor.update(difference[0], difference[1])
        #The player won't be needing this kind of updates later on
        self.player.update(difference[0], difference[1])
        
        #for enemyGroup in self.enemies:
        #    enemyGroup.update(difference[0], difference[1])
