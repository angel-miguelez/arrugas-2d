# -*- coding: utf-8 -*-

import random

import pygame
from pygame.locals import *
import sys

from characters.character import Player
from characters.enemy import Advanced2, Normal2, Basic2, Basic1, Basic0
from conf.metainfo import MetainfoManager
from effects.occlusion import Occlude
from game.director import Director
from game.scene import Scene
from map.level import Level
from menu.pause import PauseScene
from objects.door import Switch, Door
from objects.elevator import Elevator
from objects.glasses import Glasses
from objects.labcoat import LabCoat
from objects.letter import Letter


class PlayablePhase(Scene):
    """
    Base class to every playable scene
    """

    def __init__(self, nextScene):

        super().__init__(nextScene)

        self.level = None  # zone where the player can move
        self.player = None

        # All the groups we have, each of them with some different behaviour
        self.backgroundGroup = pygame.sprite.Group()  # background images or effects
        self.playerGroup = pygame.sprite.Group()
        self.npcGroup = pygame.sprite.Group()
        self.objectsGroup = pygame.sprite.Group()
        self.foregroundGroup = pygame.sprite.Group()  # e.g. visual effects (occlusion)
        self.uiGroup = []  # UI elements do not need to be sprites, they can be simple images or text

    def onEnterScene(self):
        pygame.mouse.set_visible(False)
        MetainfoManager.saveCheckpoint(self)

    def onExitScene(self):
        pass

    def events(self, events):

        for event in events:

            # Quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Return to the previous scene
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                Director().pop()

            # Pause the game
            elif event.type == KEYDOWN and event.key == K_p:
                self.playerGroup.sprites()[0].stop()
                Director().push(PauseScene())

        for object in self.objectsToEvent:
            object.events(events)

    def update(self, *args):

        for object in self.objectsToUpdate:
            object.update(*args)

    def draw(self, surface):
        surface.fill((0, 0, 0))

        self.backgroundGroup.draw(surface)
        self.level.draw(surface)

        self.objectsGroup.draw(surface)

        self.npcGroup.draw(surface)
        self.playerGroup.draw(surface)

        self.foregroundGroup.draw(surface)

        for ui in self.uiGroup:
            ui.draw(surface)


class GamePhase(PlayablePhase):

    def __init__(self, nextScene, level):
        super().__init__(nextScene)

        self.level = Level(level, 400, 300)  # Setup map structure
        self.nextScene = nextScene  # scene to load when this one is finished

        # Initialize the player
        self.player = Player((400, 300), 0.2)
        self.player.attach(self.level)  # notify the level when the player changes the position
        self.level.setPlayer(self.player)  # proper update of the level position in the world

        self.player.addCollisionGroup(self.level.getWalls())
        self.addToGroup(self.player, "playerGroup")

        # Create the vision occlusion effect
        self.occlude = Occlude()
        self.addToGroup(self.occlude, "foregroundGroup")

        # Initialize the elevator to change to the next level
        password = [random.randrange(0, 10) for _ in range(0, 4)]  # random number between 0000-9999
        elevator = Elevator(password, self.playerGroup, (self.level.getElevator()[0], self.level.getElevator()[1]))
        self.addToGroup(elevator, "objectsGroup")

        # Initialize the enemies, objects and switches of every room
        enemies = self._createEnemies(self.level.getEnemies())
        objects = self._createObjects(self.level.getObjects())
        self._createSwitches(self.level.getSwitches(), enemies, objects, password)

        # Register objects to update and event methods
        self.addToGroup([self.player, self.objectsGroup, self.npcGroup], "objectsToUpdate")
        self.addToGroup([self.player], "objectsToEvent")

    def _createEnemy(self, enemy):
        """
        Creates a specific type of enemy, based on the level data
        """

        data = enemy.split()

        if data[2] == "Basic0":
            enemy = Basic0([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls())
        elif data[2] == "Basic1":
            offset = 180
            waypoints = [(int(data[0])-offset, int(data[1])), (int(data[0]), int(data[1]))]
            spawn = [int(data[0]), int(data[1])]
            enemy = Basic1(spawn, self.playerGroup, self.level.getWalls(), waypoints, 0.3)
        elif data[2] == "Basic12":
            offset = 180
            waypoints = [(int(data[0])-offset, int(data[1])), (int(data[0]), int(data[1]))]
            spawn = [int(data[0]), int(data[1])]
            enemy = Basic1(spawn, self.playerGroup, self.level.getWalls(), waypoints, 0.1)
        elif data[2] == "Basic2":
            enemy = Basic2([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls())
        elif data[2] == "Basic4":
            enemy = Basic2([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls())
        elif data[2] == "Normal21":
            enemy = Normal2([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls(), 0.15)
        elif data[2] == "Normal22":
            enemy = Normal2([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls(), 0.1)
        elif data[2] == "Advanced2":
            enemy = Advanced2([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls())

        self.player.attach(enemy)

        return enemy

    def _createEnemies(self, data):
        """
        Creates the list of enemies for each room (each position in the list) based on the level data
        """

        enemies = []

        for enemyGroupString in data:
            enemyGroup = []

            for enemyString in enemyGroupString:
                enemy = self._createEnemy(enemyString)
                enemyGroup.append(enemy)

            enemies.append(enemyGroup)

        return enemies

    def _createObjects(self, data, itemSpawn=0.1):
        """
        Creates the list of objects for each room (each position in the list) based on the level data and the
        probability to generate an object.
        """

        objects = []
        glassesSpawned = False  # only one Glasses object

        for objectGroupString in data:
            objectGroup = []

            for objectString in objectGroupString:
                data = objectString.split()

                if data[2] == "Labcoat" and random.random() <= itemSpawn:
                    labcoat = LabCoat(self.playerGroup, (int(data[0]), int(data[1])))
                    objectGroup.append(labcoat)
                elif data[2] == "Glasses" and not glassesSpawned and random.random() <= itemSpawn:
                    glassesSpawned = True
                    glasses = Glasses(self.playerGroup, (int(data[0]), int(data[1])))
                    glasses.attach(self.occlude)  # link glasses with the effect so that it can disappear when picked up
                    objectGroup.append(glasses)

            objects.append(objectGroup)

        return objects

    def _createSwitches(self, data, enemies, objects, password):
        """
        Creates the switches and doors of every room based on the level data, links the corresponding enemies and
        objects of each one to their switches and spawns the letters of the level (they are switches since they open
        the doors when picked up)
        """

        lettersCreated = 0
        totalSwitches = len(data)

        for idx, switch in enumerate(data):
            data = [int(numeric_string) for numeric_string in switch.split()]

            remainingLoops, remainingLetters = (totalSwitches - idx - 1, 4 - lettersCreated)

            # If we have created all the letters of the level, then we can only spawn a switch in that room
            if remainingLetters == 0:
                letterOrSwitch = Switch("switch.png", (data[5], data[6]), self.playerGroup, [], lock=False)

            # Otherwise, spawn a letter with a probability of 0.5
            elif remainingLetters == remainingLoops or random.random() >= 0.5:
                digit = password[random.randrange(0, len(password))]  # retrieve a random digit from the password
                password.remove(digit)  # remove it so we do not spawn letters with the same digit
                letterOrSwitch = Letter((data[5], data[6]), self.playerGroup, digit)
                lettersCreated += 1

            # Spawn a switch with a probability of 0.5 (elif guard not satisfied)
            else:
                letterOrSwitch = Switch("switch.png", (data[5], data[6]), self.playerGroup, [], lock=False)

            entities = enemies[idx] + objects[idx] + [letterOrSwitch]  # all the entities to be activated in the room

            # Create the door of the room and the switches to open/close it
            door = Door((data[0], data[1]), self.playerGroup)
            letterOrSwitch.attach(door)  # open the door when picking the letter or pushing the switch

            offset = ((data[4] * 45) - 22)
            insideSwitch = Switch("invisible_tile.png", (data[2] + offset, data[3]), self.playerGroup, entities, visible=False, addEntities=True)

            offset = - ((data[4] * 100) - 50)  # move the outside switch to the left or right 50px
            outsideSwitch = Switch("invisible_tile.png", (data[0] + offset, data[1]), self.playerGroup, entities, active=False, visible=False)

            insideSwitch.attach(door)  # close the door on enter the room
            outsideSwitch.attach(door)  # close the door on exit the room
            insideSwitch.attach(outsideSwitch)  # activate the switch from outside after entering the room

            self.addToGroup([door, insideSwitch, outsideSwitch], "objectsGroup")
