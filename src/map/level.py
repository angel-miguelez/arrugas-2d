from turtle import pos
import pygame
import numpy as np
from map.tiles import Tile
from res.levels import *
from characters.character import *
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

        # Group of tiles that form the walls of the map
        self.walls = pygame.sprite.Group()
        # Group of tiles that form the floor of the map
        self.floor = pygame.sprite.Group()

        #self._player = Player((400, 300))
        self._player = Player((400, 300), 0.2)

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

        #Enemy array, for room number 1 the enemies would be located on the 0 position of the array so roomNumber - 1
        self.enemies = []

        #Array for switches, room number 1 the enemies would be located on the 0 position of the array so roomNumber - 1
        self.switches = []

        #Array for letters, room number 1 the enemies would be located on the 0 position of the array so roomNumber - 1
        self.letters = []

        #Array for objects
        self.objects = []

        #Coordinates to place the elevator on
        self.elevator = (0, 0)

        self.setupLevel(level_data)

    def getEnemies(self):
        return self.enemies

    def getSwitches(self):
        return self.switches
    
    def getLetters(self):
        return self.letters
    
    def getElevator(self):
        return self.elevator

    def getWalls(self):
        return self.walls
    
    def getFloor(self):
        return self.floor
    
    def getObjects(self):
        return self.objects

    def setPlayer(self, player):
        self._player = player

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

        #We divided the enemies depending on the room the spawn in
        enemyGroup = []
        objectGroup = []

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

                #Check to see if we have to add a Basic1 enemy
                if room_cell == 'R':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_1, (x, y), self.floor)

                    enemyGroup.append(str(x) + " " + str(y) + " Basic1")

                #Check to see if we have to add a Basic12 enemy
                if room_cell == 'Q':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_1, (x, y), self.floor)

                    enemyGroup.append(str(x) + " " + str(y) + " Basic12")

                #Check to see if we have to add a Basic0 enemy
                if room_cell == 'W':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_3, (x, y), self.floor)

                    enemyGroup.append(str(x) + " " + str(y) + " Basic0")
                
                #Check to see if we have to add a Basic2 enemy
                if room_cell == 'M':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)
                    
                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_4, (x, y), self.floor)

                    enemyGroup.append(str(x) + " " + str(y) + " Basic2")
                
                #Check to see if we have to add a Advanced2 enemy
                if room_cell == 'I':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)
                    
                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_3, (x, y), self.floor)

                    enemyGroup.append(str(x) + " " + str(y) + " Advanced2")

                #Check to see if we have to add a Normal2 fast enemy
                if room_cell == 'T':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)
                    
                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_5, (x, y), self.floor)

                    enemyGroup.append(str(x) + " " + str(y) + " Normal21")
                
                #Check to see if we have to add a Normal2 slow enemy
                if room_cell == 't':
                    
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)
                    
                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_5, (x, y), self.floor)

                    enemyGroup.append(str(x) + " " + str(y) + " Normal22")
                
                #Check to see if we have to add a letter in the room
                if room_cell == 'C':
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_2, (x, y), self.floor)

                    #Store letter position to add on the scene
                    self.letters.append(str(x) + " " + str(y))
                
                #Check to see if we have to add a labcoat in the room
                if room_cell == 'A':
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_2, (x, y), self.floor)

                    #Store letter position to add on the scene
                    objectGroup.append(str(x) + " " + str(y) + " Labcoat")
                
                #Check to see if we have to add glasses in the room
                if room_cell == 'B':
                    #Calculate position for the tile
                    (x, y) = self.__calculatePos(aux_x, start_row)

                    #Creating tile and adding it to the group
                    self.__setSprite(_FLOOR_2, (x, y), self.floor)

                    #Store letter position to add on the scene
                    objectGroup.append(str(x) + " " + str(y) + " Glasses")

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

        self.enemies.append(enemyGroup)
        self.objects.append(objectGroup)

    def __setupPlayerSpawn(self):
        difference = (self._playerPosX -
                      self._playerSpawnX, self._playerPosY - self._playerSpawnY)

        #Update elevator position based on the player spawn
        self.elevator = self.elevator[0] + difference[0], self.elevator[1] + difference[1]

        #Update walls and floor position based on the player spawn
        self.walls.update(difference[0], difference[1])
        self.floor.update(difference[0], difference[1])

        #Update enemies position based on the player spawn
        for groupIndex, enemyGroup in enumerate(self.enemies):
            if enemyGroup == []:
                pass
            else:
                for enemyIndex, enemy in enumerate(enemyGroup):
                    data = enemy.split()
                    enemy = str(int(data[0]) + difference[0] + 16) + \
                        " " + str(int(data[1]) + difference[1]) + " " + data[2]
                    enemyGroup[enemyIndex] = enemy
            
            self.enemies[groupIndex] = enemyGroup

        #Update switches, doors and letters position based on the player spawn
        for switchIndex, switch in enumerate(self.switches):
            data = switch.split()
            letter = self.letters[switchIndex]
            data2 = letter.split()  

            switch = str(int(data[0]) + difference[0] + 16) + \
                " " + str(int(data[1]) + difference[1] + 16) + \
                " " + str(int(data[2]) + difference[0] + 16) + \
                " " + str(int(data[3]) + difference[1] + 16) + \
                " " + str(int(data[4])) + " " + \
                str(int(data2[0]) + difference[0] + 16) + " " + \
                str(int(data2[1]) + difference[1] + 16)

            self.switches[switchIndex] = switch
        
        #Update objects position based on the player spawn
        for objectGroupIndex, objectGroup in enumerate(self.objects):
            for objectIndex, object in enumerate(objectGroup):
                data = object.split()

                object = str(int(data[0]) + difference[0] + 16) + \
                    " " + str(int(data[1]) + difference[1] + 16) + " " + data[2]
                
                objectGroup[objectIndex] = object


            self.objects[objectGroupIndex] = objectGroup

    def setupLevel(self, layout):
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
                    self._playerSpawnX = x
                    self._playerSpawnY = y

                    self.__setSprite(_FLOOR_2, (x, y), self.floor)
                
                #Check to see if we have to add a player tile
                if cell == 'E':
                    #Set floor tile
                    self.__setSprite(_FLOOR_2, (x, y), self.floor)

                    #Get elevator position
                    self.elevator = (x + 64, y)
                
                #Check to see if we have a door
                if cell == 'D':
                    insideInt = -1

                    #Get the room we want to add
                    while True:
                        num = np.random.randint(0, room_num)
                        if self.levels[num] == False:
                            self.levels[num] = True
                            break
                    
                    #Get the room from the list of rooms based on the random number
                    room = rooms_1[num]

                    if inside:
                        insideInt = 1
                        #The empty space on the map is to the right of the door
                        col = col_index + 1

                        #Save positions for the switches and the door
                        self.switches.append(
                            str(x) + " " + str(y) + " " + str(col * tile_size) + " " + str(y) + " " + str(insideInt))

                        #Add the room
                        self.__addRoom(room, (row_index, col), inside)
                        
                    else:
                        insideInt = 0
                        #The empty space on the map is to the left of the door
                        col = col_index - 1

                        #Save positions for the switches and the door
                        self.switches.append(
                            str(x) + " " + str(y) + " " + str(col * tile_size) + " " + str(y) + " " + str(insideInt))

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
            #for enemyGroup in self.enemies:
            #    enemyGroup.draw(self.display_surface)  # Draw the enemies
    
    def updateObserver(self, subject: Player):
        newPos = subject.getPos()
        difference = (self.worldShiftX -
                      newPos[0], self.worldShiftY - newPos[1])

        self.worldShiftX = newPos[0]
        self.worldShiftY = newPos[1]

        self.walls.update(difference[0], difference[1])
        self.floor.update(difference[0], difference[1])
        
        #for enemyGroup in self.enemies:
        #    enemyGroup.update(difference[0], difference[1])
