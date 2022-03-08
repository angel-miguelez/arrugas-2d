# -*- coding: utf-8 -*-

import pygame.key

from characters.entity import Entity
from characters.character import *
from game.director import Director
from map.tiles import Tile
from utils.resourcesmanager import *
import itertools


class Enemy(Character, Entity):
    """
    Every enemy is a character that observes the Player position via the Entity class
    """

    def __init__(self, imageFile, coordFile, sheetDimension, position, playerGroup, wallsGroup, scale, speed, animationDelay):
        Character.__init__(self, imageFile, coordFile, sheetDimension, position, scale, speed, animationDelay)
        Entity.__init__(self, position)
        Entity.setPlayer(self, playerGroup.sprites()[0])

        self.addCollisionGroup(playerGroup)
        self.addCollisionGroup(wallsGroup)

    def update(self, time):
        Character.update(self, time)
        self.position = self.x, self.y  # the (x,y) of Character must be consistent with position of Entity
        self.rect.center = self.position  # enemy need to update its rect because its position on the screen varies

    def updateObserver(self, subject):
        Entity.updateObserver(self, subject)
        self.x, self.y = self.position  # the (x,y) of Character must be consistent with position of Entity

    def onCollisionEnter(self, collided):
        Character.onCollisionEnter(self, collided)

        if isinstance(collided, Tile):
            self.position = self.lastPos  # the (x,y) of Character must be consistent with position of Entity

        if isinstance(collided, Player):
            Director().pop(fade=True)

    def remove(self):
        """
        Removes the object from all the groups of the scene, so it disappears completely
        """

        scene = Director().getCurrentScene()
        scene.removeFromGroup(self, "npcGroup")


        self._player.detach(self)
        
    def add(self, enemy, group):
        """
        Removes the object from all the groups of the scene, so it disappears completely
        """

        scene = Director().getCurrentScene()
        scene.addToGroup(enemy, group)


        self._player.attach(self)


class Basic0(Enemy):
    """
    Worm enemy, it only stands and updates its animation
    """

    def __init__(self, position, playerGroup, wallsGroup):
        Enemy.__init__(self, 'B0.png', 'coordBasic0.txt', [7], position, playerGroup, wallsGroup, (32, 32), 0.3, 7)

    def move(self):
        return 0, 0


class Basic1(Enemy):
    """
    Ratt enemy, it moves from one point to another in loop
    """

    def __init__(self, position, playerGroup, wallsGroup, waypoints, speed):
        if(speed>=0.2):
            Enemy.__init__(self, 'B1.1.png', 'coordBasic1.1.txt', [6,6], position, playerGroup, wallsGroup, (32, 32), speed, 5)
        else:
            Enemy.__init__(self, 'B1.2.png', 'coordBasic1.2.txt', [6,6], position, playerGroup, wallsGroup, (32, 32), speed, 5)

        self.waypoints = itertools.cycle(waypoints)  # points of reference to go from/to in loop
        self.target = next(self.waypoints)  # current point target
        self.targetOffset = pygame.math.Vector2(0, 0)  # offset to add to the target position when the player moves
        self.targetRadius = 20  # distance to the target to slow down the speed
        self._lastDistance = 0  # to check if the enemy cannot reach the target due to int(vel) = (0, 0) or collisions

        self.movement = self.target[0] > self.position[0]  # if the first target is at the right, move to the right
        self.posture = not self.movement

    def _changeTarget(self):
        """
        Changes the target point, updating the movement direction and the sprite too
        """
        self.target = next(self.waypoints)  # change target
        self.movement = not self.movement  # change to the opposite direction
        self.posture = not self.posture  # change to the opposite sprite

    def move(self):

        dir = (self.target + self.targetOffset) - self.position  # get the direction to the target
        distance = dir.length()  # distance to the target
        vel = pygame.math.Vector2(0, 0)

        # If the enemy has reached or overpass the target, change to the other one
        if (self.movement == LEFT and dir[0] > 0) or (self.movement == RIGHT and dir[0] < 0):
            self._changeTarget()

        # If we're approaching the target, we slow down
        elif distance <= self.targetRadius:
            dir.normalize_ip()
            vel = dir * (distance / self.targetRadius * self.speed)

        # Otherwise, move with max speed
        else:
            dir.normalize_ip()
            vel = dir * self.speed

        # If the enemy has stuck in a position due to collisions or other events
        if self._lastDistance == distance:
            self._changeTarget()

        self._lastDistance = distance

        return vel

    def updateObserver(self, subject):
        super().updateObserver(subject)
        self.targetOffset -= pygame.math.Vector2(self.offset)  # update the target pos




class Basic2(Enemy):
    """
    Wizard that does something when the Player enter its radius
    """

    def __init__(self, position, playerGroup, wallsGroup):
        Enemy.__init__(self, 'B2.png', 'coordBasic2.txt', [10], position, playerGroup, wallsGroup, (148, 120), 0.3, 5)
        self.radius = 200
        self.isPlayerClose = False

    def move(self):

        # Get the direction to the player, and if the distance is less than the radius, change the state
        dir = pygame.math.Vector2(self._player.rect.center) - pygame.math.Vector2(self.position)
        self.isPlayerClose = dir.length() <= self.radius

        return 0, 0

    def updateImage(self):
        if not self.isPlayerClose:
            self.subPosture = 0

        super().updateImage()


class Basic4(Enemy):
    """
    Worm enemy, it only stands and updates its animation
    """

    def __init__(self, position, playerGroup, wallsGroup, timeToShot = 120, delayConsecutiveShots = 30, treeSprite = 1):
        Enemy.__init__(self, 'blueTree.png', 'coordBlueTree.txt', [1, 1], position, playerGroup, wallsGroup, (42, 42), 0.3, 7)
        self.timeToShot = timeToShot # time between 2 shots
        self.delayConsecutiveShots = delayConsecutiveShots # time between 2 shots
        self.counterToShot = 0  # counter time
        self.playerGroup = playerGroup
        self.wallsGroup = wallsGroup
        self.posture = treeSprite
        
    def move(self):
        self.counterToShot += 1
        if self.timeToShot == self.counterToShot:
             bat1 = Bat([self.x, self.y], self.playerGroup, self.wallsGroup, RIGHT)
             bat2 = Bat([self.x, self.y], self.playerGroup, self.wallsGroup, LEFT)
             bat3 = Bat([self.x, self.y], self.playerGroup, self.wallsGroup, UP)
             bat4 = Bat([self.x, self.y], self.playerGroup, self.wallsGroup, DOWN)
             self.add([bat1, bat2, bat3, bat4], "npcGroup")

        if (self.timeToShot + self.delayConsecutiveShots) == self.counterToShot:
             self.counterToShot = 0
             bat1 = Bat([self.x, self.y], self.playerGroup, self.wallsGroup, RIGHT)
             bat2 = Bat([self.x, self.y], self.playerGroup, self.wallsGroup, LEFT)
             bat3 = Bat([self.x, self.y], self.playerGroup, self.wallsGroup, UP)
             bat4 = Bat([self.x, self.y], self.playerGroup, self.wallsGroup, DOWN)
             self.add([bat1, bat2, bat3, bat4], "npcGroup")

        return 0, 0



class Bat(Enemy):
    """
    Bird that runs against the Player when it walks by its side
    """

    def __init__(self, position, playerGroup, wallsGroup, direction):
        Enemy.__init__(self, 'Bat.png', 'coordBat.txt', [4, 4, 4, 4], position, playerGroup, wallsGroup, (32, 32), 0.2, 5)
        self.direction = direction
        self.destruction = False
        
    def move(self):
        if self.destruction == True: 
            self.remove() #CAMBIAR 
            return 0, 0

        # If the enemy is not active, set an IDLE sprite looking to a specific direction
        if self.direction == LEFT:
            self.posture = 0
            return -self.speed, 0
        if self.direction == RIGHT:
            self.posture = 1
            return self.speed, 0
        if self.direction == UP:
            self.posture = 2
            return 0, -self.speed
        if self.direction == DOWN:
            self.posture = 3
            return 0, self.speed

    def onCollisionEnter(self, collided):
        Character.onCollisionEnter(self, collided)

        if isinstance(collided, Tile):
            self.destruction=True
            self.position = self.lastPos

        if isinstance(collided, Player):
            Director().pop(fade=True)


class Normal2(Enemy):
    """
    Enemy that follows the Player across the room
    """

    def __init__(self, position, playerGroup, wallsGroup):
        Enemy.__init__(self, 'N2.2.png', 'coordNormal2.2.txt', [3,3,3,3], position, playerGroup, wallsGroup, (32, 50), 0.1, 10)
        self.area = 300  # area of vision of the enemy
        self._stopDistance = 5

    def move(self):

        playerx, playery = self._player.rect.center  # get the player position
        xDistance, yDistance = self.x - playerx, self.y - playery  # calculate the distance in each direction

        # If the player is inside the area vision of the enemy, follow it
        if abs(xDistance) < self.area and abs(yDistance) < self.area:
            if yDistance > self._stopDistance:
                self.movement = UP
                self.posture = 2
                return 0, -self.speed
            elif yDistance < self._stopDistance:
                self.movement = DOWN
                self.posture = 3
                return 0, self.speed
            elif xDistance > self._stopDistance:
                self.movement = LEFT
                self.posture = 0
                return -self.speed, 0
            elif xDistance < self._stopDistance:
                self.movement = RIGHT
                self.posture = 1
                return self.speed, 0

        self.movement = IDLE
        return 0, 0




class Advanced2(Enemy):
    """
    Bird that runs against the Player when it walks by its side
    """

    def __init__(self, position, playerGroup, wallsGroup):
        Enemy.__init__(self, 'A2.png', 'coordA2.txt', [3, 10, 8, 3, 10, 8], position, playerGroup, wallsGroup, (32, 32), 0.2, 5)

        self.deathcounter=0
        self.activated = False
        self.destruction = False

    def move(self):

        # If the enemy is not active, set an IDLE sprite looking to a specific direction
        if not self.activated:
            if self.movement == RIGHT:
                self.posture = 0
            if self.movement == LEFT:
                self.posture = 3

        # Otherwise, set movement animations
        else:
            if self.movement == RIGHT:
                if not self.destruction:
                    self.posture = 1
                else:
                    self.deathcounter += 1
                    self.posture = 2
            else:
                if not self.destruction:
                    self.posture = 4
                else:
                    self.deathcounter += 1
                    self.posture = 5

        if self.deathcounter==30: 
            self.remove() #CAMBIAR 
            return -self.speed, 0

        if self.activated:
            if self.movement==RIGHT:
                return self.speed, 0
            else: return -self.speed, 0

        # If the player is not close enough, the enemy is inactive
        elif abs(self._player.rect.center[1] - self.position[1]) > 5 and not self.activated:
            self.movement = IDLE
            return 0, 0

        # Otherwise, it tries to hit the player moving horizontally
        else:
            self.activated = True
            if self._player.rect.center[0] > self.x:
                self.movement = RIGHT
                return self.speed, 0
            else:
                self.movement = LEFT
                return -self.speed, 0

    def onCollisionEnter(self, collided):
        Character.onCollisionEnter(self, collided)

        if isinstance(collided, Tile):
            self.destruction=True
            self.position = self.lastPos  

        if isinstance(collided, Player):
            self.destruction=True
            Director().pop(fade=True)
