# -*- coding: utf-8 -*-

import pygame.key

from game.director import Director
from game.interactive import Interactive
from map.tiles import Tile
from characters.npc import DialogueCharacter
from utils.resourcesmanager import *
from utils.observer import Subject

# Movement direction constants
LEFT, RIGHT, UP, DOWN = 0, 1, 2, 3
IDLE = 4


class Character(pygame.sprite.Sprite, Interactive):
    """
    Class that represents every character in the game
    """

    def __init__(self, imageFile, coordFile, sheetDimension, position, scale, speed, animationDelay):
        """
        imageFile -> file with image data
        coordFile -> File with all the coordinates of the sprites from imageFile
        sheetDimension -> array with the number of different sprites. ex: [4, 4] 2 positions with 4 different sprites each
        coordScreen -> coordinates on screen where sprite is initialized
        scale -> size of the sprites
        speed -> speed of the player
        animationDelay -> delay on each movement of the characters
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

        # Initialize sprite image and rect
        self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][self.subPosture]), scale)
        self.rect = self.image.get_rect()
        self.scale = scale  # size of the image

        # Initialize collision system to collide with the walls
        Interactive.__init__(self, self.rect)

        # Initial position on the screen
        self.x, self.y = (position[0], position[1])
        self.lastPos = (self.x, self.y)  # used to revert the last movement if it collided with a wall
        self.rect.center = self.x, self.y

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

        # If it has collided with a wall, it returns to the previous position
        if isinstance(collided, Tile):
            self.x, self.y = self.lastPos
            self.objectsEnterCollision.remove(collided)  # so if still moves to the same direction we can get it again

    def pillEffect(self):
        self.speed = self.speed * 0.5


class Player(Character, Subject):
    """
    Class that represents the playable character
    """""

    def __init__(self, position, speed=1, animationDelay=5):
        Subject.__init__(self)
        Character.__init__(self, 'character.png', 'coordMan.txt', [3, 3, 3, 3], position, (25, 29), speed, animationDelay)

        # We use a new rect that is placed at the bottom body-upper legs of the sprite to detect collisions
        legsRect = self.rect.copy()
        legsRect.inflate_ip(-5, -13)
        legsRect.bottom = self.rect.bottom
        legsRect.left = self.rect.left + (self.rect.width - legsRect.width) / 2
        self.changeCollisionRect(legsRect)

        # Load the movement bindings from the configuration file
        self.MOVE_UP, self.MOVE_DOWN, self.MOVE_RIGHT, self.MOVE_LEFT = ConfManager().getPlayerMovementBinds()
        self.lastMovements = [IDLE]  # ordered sequence of movement keys pressed by the user (more info in move method)

        self.eventsEnabled = True

    def increaseSpeed(self):
        self.speed *= 1.5
        self.animationDelay /= 1.5

    def stop(self):
        self.lastMovements = [IDLE]
        self.movement = IDLE
        self.eventsEnabled = False
    
    def start(self):
        self.lastMovements = [IDLE]
        self.movement = IDLE
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
        else:
            self.subPosture = 0

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

    def updateImage(self):
        # The player does not have an IDLE animation, so we must overwrite to set always the same sprite in that case
        if self.movement == IDLE:
            image = self.sheet.subsurface(self.sheetCoord[self.posture][0])
            self.image = pygame.transform.scale(image, self.scale)
        else:
            super().updateImage()

    def update(self, time):
        self.movement = self.lastMovements[-1]  # the last key pressed by the user
        Character.update(self, time)
        self.notify()  # notify to draw the rest of entities properly

    def getPos(self):
        return self.x, self.y

