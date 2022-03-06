# -*- coding: utf-8 -*-
from abc import ABC
from pickle import TRUE
import pygame.key
from characters.entity import Entity

from characters.entity import Entity
from game.interactive import Interactive
from game.director import Director
from map.tiles import Tile
from utils.resourcesmanager import *
import itertools
from utils.observer import Subject
import math

# Movement direction constants
LEFT, RIGHT, UP, DOWN = 0, 1, 2, 3
IDLE = 4
UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT = 5, 6, 7, 8

DIAG_FACTOR = math.sqrt(2) / 2  # avoid diagonal movements been faster than the others


class Character(pygame.sprite.Sprite, Interactive):
    """
    Class that represents every character in the game
    """

    def __init__(self, imageFile, coordFile, sheetDimension, position, scale, speed, animationDelay, updateByTime):
        """
        imageFile -> file with image data
        coordFile -> File with all the coordinades of the sprites from imageFile
        sheetDimension -> array with the number of diferent sprites. ex: [4, 4] 2 positions with 4 different sprites each position
        coordScreen -> coordinates on screen where sprite is initialized
        scale -> size of the sprites
        speed -> speed of the player
        animationDelay -> delay on each movement of the characters
        updateByTime -> if sprite is updated every moment(basic0) or updated while moving(player)
        walls -> group of sprites that the player can not step over
        """

        pygame.sprite.Sprite.__init__(self)

        # Load and split the sprite sheet
        self.sheet = ResourcesManager.loadImage(imageFile, -1)
        data = ResourcesManager.loadCoordFile(coordFile)
        data = list(map(lambda x: int(x), data.split()))
        self.sheetCoord = self._processSpriteSheet(data, sheetDimension)

        # Sprite posture
        self.posture = LEFT
        self.subPosture = 0  # column position in the posture (row)
        self.animationDelay = animationDelay  # time to wait to update the next image
        self.timeToUpdateSprite = 0  # counter

        self.updateByTime = updateByTime

        # Initialize sprite image and rect
        self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][self.subPosture]), scale)
        self.rect = self.image.get_rect()
        self.scale = scale  # size of the image

        # Initialize collision system to collide with the walls
        Interactive.__init__(self, self.rect)

        # Initial position on the screen
        self.x, self.y = (position[0], position[1])
        self.lastPos = (self.x, self.y)  # used to revert the last movement if it collided with a wall
        self.rect.left = self.x
        self.rect.bottom = self.y

        # Movement related variables
        self.movement = IDLE
        self.xShift, self.yShift = (0, 0)
        self.speed = speed

    def _processSpriteSheet(self, sheet, sheetDimension):
        """
        Iterates over the sheet saving the different sprites into a list
        """

        out = []
        cont = 0

        for line in range(0, len(sheetDimension)):
            out.append([])  # create a new posture
            tmp = out[line]

            for position in range(1, sheetDimension[line] + 1):  # iterate over the subpostures
                tmp.append(Rect((sheet[cont], sheet[cont + 1]), (sheet[cont + 2], sheet[cont + 3])))
                cont += 4

        return out

    def updateImage(self):
        """
        Updates the current image of the sprite, if the counter has reached 0
        """

        self.timeToUpdateSprite -= 1
        if self.timeToUpdateSprite > 0:  # we have to wait more time to update the image
            return

        self.timeToUpdateSprite = self.animationDelay  # reset the counter
        self.subPosture += 1  # go to the next subposture in the row

        # If we have reached the last subposture, return to the initial one
        if self.subPosture >= len(self.sheetCoord[self.posture]):
            self.subPosture = 0

        # Update the image
        image = self.sheet.subsurface(self.sheetCoord[self.posture][self.subPosture])
        self.image = pygame.transform.scale(image, self.scale)

        # no movement is being done
        if self.updateByTime == 0 and self.movement == IDLE:
            self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][0]), self.scale)

    def move(self):
        """
        Manages the movement of the character, so each class must implement it since it can depend on the user input,
        player position, target points... It returns the x and y shift.
        """
        raise NotImplementedError("Movement logic not implemented.")

    def update(self, time):

        # Update the movement
        self.xShift, self.yShift = self.move()
        self.xShift = int(self.xShift * time)
        self.yShift = int(self.yShift * time)

        self.lastPos = (self.x, self.y)
        self.x += self.xShift
        self.y += self.yShift

        # Update the sprite image
        self.updateImage()

        # "Pre-move" to check if it is colliding with a wall, so we should undo the movement
        self.collisionRect.left += self.xShift  # move the collision rect to the future position
        self.collisionRect.bottom += self.yShift
        self.updateCollisions()  # check collisions
        self.collisionRect.left -= self.xShift  # return the collision rect to the current position
        self.collisionRect.bottom -= self.yShift

    def onCollisionEnter(self, collided):

        if isinstance(collided, Tile):
            self.x, self.y = self.lastPos
            self.objectsEnterCollision.remove(collided)

    def pillEffect(self):
        self.speed = self.speed * 0.5


class Player(Character, Subject):
    """
    Class that represents the playable character
    """""

    def __init__(self, position, speed=1, animationDelay=5):
        Subject.__init__(self)
        Character.__init__(self, 'character.png', 'coordMan.txt', [3, 3, 3, 3], position, (25, 29),
                           speed, animationDelay, 0)

        # We use a new rect that is placed at the bottom body-upper legs of the sprite to detect collisions
        legsRect = self.rect.copy()
        legsRect.inflate_ip(-5, -13)
        legsRect.bottom = self.rect.bottom - 2
        legsRect.left = self.rect.left + (self.rect.width - legsRect.width) / 2
        self.changeCollisionRect(legsRect)

        # Load the movement bindings from the configuration file
        self.MOVE_UP, self.MOVE_DOWN, self.MOVE_RIGHT, self.MOVE_LEFT = ConfManager().getPlayerMovementBinds()
        self.lastMovements = [IDLE]  # ordered sequence of movement keys pressed by the user (more info in move method)

        self.eventsEnabled = True

        self.hasPills = 0

    def increaseSpeed(self):
        self.speed *= 1.5
        self.animationDelay /= 1.5

    def disableEvents(self):
        self.eventsEnabled = False

        # Stop the player
        self.lastMovements = [IDLE]
        self.movement = IDLE

    def enableEvents(self):
        self.eventsEnabled = True

    def move(self):
        xShift, yShift = (0, 0)
        if self.movement == LEFT:
            self.posture = LEFT
            xShift = -self.speed
        elif self.movement == RIGHT:
            self.posture = RIGHT
            xShift = self.speed
        elif self.movement == UP:
            self.posture = UP
            yShift = -self.speed
        elif self.movement == DOWN:
            self.posture = DOWN
            yShift = self.speed
        return xShift, yShift

    def readMovementEvent(self, event):
        """
        The player can press multiple keys in a row, but the current movement will correspond only to the last key
        pressed. We save the order in which these keys were pressed, so if the last one (current movement) is released
        we recover the previous movement.

        For example, if the player is going to the left and presses the MOVE_RIGHT button (without releasing MOVE_LEFT),
        the movement will be to the right. Now, if it releases MOVE_RIGHT, the movement will back to be to the left.
        This way, when a key is pressed we append it to the list, and if is released the key is removed from it.
        """

        # Update the current movement to the current key pressed
        if event.type == KEYDOWN:

            if event.key == self.MOVE_LEFT:
                self.movement = LEFT
                self.lastMovements.append(LEFT)
            elif event.key == self.MOVE_RIGHT:
                self.movement = RIGHT
                self.lastMovements.append(RIGHT)
            elif event.key == self.MOVE_UP:
                self.movement = UP
                self.lastMovements.append(UP)
            elif event.key == self.MOVE_DOWN:
                self.movement = DOWN
                self.lastMovements.append(DOWN)

        # Remove from the list the key, we have to check if it is there in case another object got control of the events
        # and we did not capture the realising
        elif event.type == KEYUP:

            if event.key == self.MOVE_LEFT and LEFT in self.lastMovements:
                self.lastMovements.remove(LEFT)
            elif event.key == self.MOVE_RIGHT and RIGHT in self.lastMovements:
                self.lastMovements.remove(RIGHT)
            elif event.key == self.MOVE_UP and UP in self.lastMovements:
                self.lastMovements.remove(UP)
            elif event.key == self.MOVE_DOWN and DOWN in self.lastMovements:
                self.lastMovements.remove(DOWN)

    def events(self, events):

        if not self.eventsEnabled:
            self.movement = IDLE
            return

        for event in events:
            self.readMovementEvent(event)

    def update(self, time):
        self.movement = self.lastMovements[-1]  # the last key pressed by the user
        Character.update(self, time)
        self.notify()  # notify to draw the level properly

    def getPos(self):
        return self.x, self.y

    def getPill(self):
        self.hasPills=self.hasPills+1

    def usePill(self, grupo):
        #if self.hasPills==0:
            #Sonido incorrecto
        #else:
        if self.hasPills>0:
            self.hasPills=self.hasPills-1
            grupo.pillEffect()
     

class Enemy(Character, Entity):

    def __init__(self, imageFile, coordFile, sheetDimension, position, playerGroup, wallsGroup, scale, speed, animationDelay, updateByTime):
        Character.__init__(self, imageFile, coordFile, sheetDimension, position, scale, speed, animationDelay, updateByTime)
        Entity.__init__(self)
        Entity.setPlayer(self, playerGroup.sprites()[0], position)

        self.addCollisionGroup(playerGroup)
        self.addCollisionGroup(wallsGroup)

    def update(self, time):
        Character.update(self, time)

        self.position = self.x, self.y
        self.rect.center = self.position

        # self.position = self.position[0] + self.xShift, self.position[1] + self.yShift
        # self.x, self.y = self.position

    def updateObserver(self, subject):
        Entity.updateObserver(self, subject)
        self.x, self.y = self.position
        # self.position = (self.position[0] + self.xShift, self.position[1] + self.yShift)

    def onCollisionEnter(self, collided):
        Character.onCollisionEnter(self, collided)

        if isinstance(collided, Tile):
            self.position = self.lastPos

        if isinstance(collided, Player):
            Director().pop()

# -------------------------------------------------
# Basic enemy 0 class (worm)


class Basic0(Enemy):

    def __init__(self, position, playerGroup, wallsGroup):
        Enemy.__init__(self, 'B0.png', 'coordBasic0.txt', [7], position, playerGroup, wallsGroup, (32, 32), 0.3, 7, 0.5)

    def move(self):
        return 0, 0

# -------------------------------------------------
# Basic enemy 1 class (ratt)

class Basic1(Enemy):
    def __init__(self, position, waypoints, speed, playerGroup,wallsGroup):
        Enemy.__init__(self, 'B1.1.png', 'coordBasic1.1.txt', [6,6], position, playerGroup,wallsGroup, (32, 32), speed, 5, 0.5)
        Entity.__init__(self)
        self.setPlayer(playerGroup.sprites()[0], position)

        self.target_radius = 20
        self.waypoints = itertools.cycle(waypoints)
        self.target = next(self.waypoints)
        self.targetOffset = pygame.math.Vector2(0, 0)

        self._lastDistance = 0  # to check if the enemy cannot reach the target due to int(vel) = (0, 0) or collisions

    def move(self):
        heading = (self.target + self.targetOffset) - self.position

        if heading[0] < 0:
            self.movement = LEFT
            self.posture = 1
        else:
            self.movement = RIGHT
            self.posture = 0

        distance = heading.length()  # Distance to the target.
        vel = pygame.math.Vector2(0, 0)

        if (self.movement == LEFT and heading[0] > 0) or (self.movement == RIGHT and heading[0] < 0):  # We're closer than 2 pixels.
            # Increment the waypoint index to swtich the target.
            # The modulo sets the index back to 0 if it's equal to the length.
            self.target = next(self.waypoints)
        elif distance <= self.target_radius:
            # If we're approaching the target, we slow down.
            heading.normalize_ip()
            vel = heading * (distance / self.target_radius * self.speed)
        else:  # Otherwise move with max_speed.
            heading.normalize_ip()
            vel = heading * self.speed

        if self._lastDistance == distance:
            self.target = next(self.waypoints)
        self._lastDistance = distance

        return vel

    def updateObserver(self, subject):
        super().updateObserver(subject)
        self.targetOffset -= pygame.math.Vector2(self.offset)


# -------------------------------------------------
# Basic enemy 2 class (wizard)


class Basic2(Enemy):
    def __init__(self, position, radius, playerGroup, wallsGroup):
        Entity.__init__(self)
        # called constructor of father class
        self.radius = radius
        Enemy.__init__(self, 'B2.png', 'coordBasic2.txt', [10], position, playerGroup, wallsGroup, (148, 120), 0.3, 5, 0.5)
        self.isPlayerClose = False

    def move(self):
        target = pygame.math.Vector2(self._player.rect.center)
        heading = target - pygame.math.Vector2(self.position)
        distance = heading.length()
        heading.normalize_ip()
        self.isPlayerClose = distance <= self.radius
        return 0, 0

    def updateImage(self):
        if not self.isPlayerClose:
            self.subPosture = 0

        super().updateImage()

# -------------------------------------------------
# Normal enemy 2 (cactus)

class Normal2(Enemy):
    "Normal2 enemy 3"
    def __init__(self, position, playerGroup, wallsGroup):
        # called constructor of father class
        Enemy.__init__(self, 'N2.2.png', 'coordNormal2.2.txt', [3,3,3,3], position, playerGroup, wallsGroup, (32, 50), 0.1, 10, 0)
        self.area = 300

    def move(self):
        # tracked player
        # area where the player is going to be tracked
        playerx, playery = (self._player.rect.left, self._player.rect.bottom)

        xShift, yShift = (0,0)
        if (abs(self.rect.left - playerx) < self.area) and (abs(self.rect.bottom - playery) < self.area):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
            if ((self.rect.left - playerx) == 0) and ((self.rect.bottom - playery) == 0):
                self.movement = IDLE
            elif ((self.rect.left - playerx) >= 0) and ((self.rect.bottom - playery) > 0):
                self.movement = UP
                self.posture = 2
                yShift = -self.speed
            elif ((self.rect.left - playerx) <= 0) and ((self.rect.bottom - playery) < 0):
                self.movement = DOWN
                self.posture = 3
                yShift = self.speed
            elif ((self.rect.left - playerx) < 0) and ((self.rect.bottom - playery) >= 0):
                self.movement = RIGHT
                self.posture = 1
                xShift = self.speed
            elif ((self.rect.left - playerx) > 0) and ((self.rect.bottom - playery) <= 0):
                self.movement = LEFT
                self.posture = 0
                xShift = -self.speed
        else:
             self.movement = IDLE

        return xShift, yShift

# -------------------------------------------------
# Advanced enemy 2

class Advanced2(Enemy):
    def __init__(self, position, playerGroup, wallsGroup, orientation):
        # called constructor of father class
        Enemy.__init__(self, 'A2.png', 'coordA2.txt', [3, 10, 8, 3, 10, 8], position, playerGroup, wallsGroup, (32, 32), 0.2, 5, 0.5)
        self.enemy = playerGroup.sprites()[0]
        self.looking = orientation
        self.activation = False
        self.destruction = False

    def move(self):

        if not self.activation:  # No movement is being done
            if self.movement == RIGHT:
                self.posture = 0
            if self.movement == LEFT:
                self.posture = 3
        else:  # Update the image
            if self.movement == RIGHT:
                if not self.destruction:
                    self.posture = 1
                else:
                    self.posture = 2
            if self.movement == LEFT:
                if not self.destruction:
                    self.posture = 4
                else:
                    self.posture = 5

        if abs(self._player.rect.bottom - self.position[1]) > 5 and not self.activation:
            self.movement = IDLE
            return 0, 0

        self.activation = True
        if self._player.rect.left > self.x:
            self.movement = RIGHT
            return self.speed, 0

        else:
            self.movement = LEFT
            return -self.speed, 0

    # def onCollisionEnter(self, collided):
    #
    #     if isinstance(collided, Tile):
    #         self.x, self.y = self.lastPos
    #         self.objectsEnterCollision.remove(collided)
    #         return True
    #
    #     elif isinstance(collided, Player):
    #         self.destruction = True


