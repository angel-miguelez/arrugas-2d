# -*- coding: utf-8 -*-

import random

import pygame

from effects.occlusion import Occlude
from game.director import Director

from map.level import Level

from characters.npc import ElderCharacter, NurseCharacter
from characters.character import Player
from characters.enemy import Basic0, Basic1, Normal2, Basic2, Basic4, Advanced2
from objects.door import Door, Switch
from objects.elevator import Elevator

from objects.glasses import Glasses
from objects.labcoat import LabCoat
from objects.letter import Letter
from phase.intro02 import Scene02Intro
from phase.playable import PlayablePhase

from res.levels import *


class PhaseTest(PlayablePhase):
    """
    Fase usada para probar cosas
    """

    def __init__(self):

        super().__init__()

        # Level
        self.level = Level(basic_layout, 400, 300)  # Setup map structure
        #self.level = Level(basic_layout_2, 400, 300)  # Setup map structure for second level

        # Player
        self.player = Player((400, 300), 0.3)
        self.player.attach(self.level)
        self.player.addCollisionGroup(self.level.getWalls())
        self.addToGroup(self.player, "playerGroup")
        self.level.setPlayer(self.player)

        # NPC
        speaker = ElderCharacter((800, 400), self.playerGroup)
        nurse = NurseCharacter((800, 600), self.playerGroup)
        self.player.addCollisionGroup(self.npcGroup)
        self.addToGroup([speaker, nurse], "npcGroup")

        # Enemies
        # for enemyGroup in self.level.getEnemies():
        #     if enemyGroup == []:
        #         pass
        #     else:
        #         for enemy in enemyGroup:
        #             self.createEnemy(enemy)

        #basic0 = Basic0([450, 300], self.playerGroup, self.level.getWalls())
        #self.addToGroup(basic0, "npcGroup")
        #self.player.attach(basic0)

        waypoints = [(320, 400), (500, 400)]
        spawn = [500, 400]
        basic1 = Basic1(spawn, self.playerGroup, self.level.getWalls(), waypoints, 0.2)
        self.addToGroup(basic1, "npcGroup")

        # basic2 = Basic2([1000, 500], self.playerGroup, self.level.getWalls())
        # self.addToGroup(basic2, "npcGroup")
        # self.player.attach(basic2)

        #normal2 = Normal2([850, 800], self.playerGroup, self.level.getWalls())
        #self.addToGroup(normal2, "npcGroup")
        #self.player.attach(normal2)
        
        # basic4 = Basic4([450, 330], self.playerGroup, self.level.getWalls())
        # self.addToGroup(basic4, "npcGroup")
        # self.player.attach(basic4)

        advanced2 = Advanced2([850, 800], self.playerGroup, self.level.getWalls())
        self.addToGroup(advanced2, "npcGroup")
        self.player.attach(advanced2)

        password = [random.randrange(0, 10) for _ in range(0, 4)]  # random number between 0000-9999

        # Adding the doors, switches and letters with the code to the scene
        lettersCreated = 0
        totalSwitches = len(self.level.getSwitches())

        for idx, switch in enumerate(self.level.getSwitches()):
            aux = switch.split()
            data = [int(numeric_string) for numeric_string in aux]

            door = Door((data[0], data[1]), self.playerGroup)
            switch = Switch("invisible_tile.png", (data[2], data[3]), self.playerGroup, "enter", visible=False)
            if data[4]:
                switch1 = Switch("invisible_tile.png", (data[0] - 50, data[1]), self.playerGroup, "exit", active=False, visible=False)
            else:
                switch1 = Switch("invisible_tile.png", (data[0] + 50, data[1]), self.playerGroup, "exit", active=False, visible=False)

            remainingLoops = totalSwitches - idx - 1
            remainingLetters = 4 - lettersCreated
            if remainingLetters == 0:
                letterOrSwitch = Switch("switch.png", (data[5], data[6]), self.playerGroup, lock=False)
            elif remainingLetters == remainingLoops or random.random() >= 0.5:
                letterOrSwitch = Letter((data[5], data[6]), self.playerGroup, password[lettersCreated])
                lettersCreated += 1
            else:
                letterOrSwitch = Switch("switch.png", (data[5], data[6]), self.playerGroup, lock=False)

            switch.attach(door)
            switch.attach(switch1)
            switch1.attach(door)
            letterOrSwitch.attach(door)
            self.addToGroup([letterOrSwitch, door, switch, switch1], "objectsGroup")

        assert lettersCreated == 4

        elevator = Elevator(password, self.playerGroup, (self.level.getElevator()[0], self.level.getElevator()[1]))
        self.addToGroup(elevator, "objectsGroup")

        #Create occlude effect
        occlude = Occlude()

        #Set threshold for item spawn
        threshold = 0.1

        #Add all the objects to the scene
        for object in self.level.getObjects():
            data = object.split()
            
            if data[2] == "Labcoat":
                if random.random() <= threshold:
                    labcoat = LabCoat(self.playerGroup, (int(data[0]), int(data[1])))
                    self.addToGroup(labcoat, "objectsGroup")
            elif data[2] == "Glasses":
                if random.random() <= threshold:
                    glasses = Glasses(self.playerGroup, (int(data[0]), int(data[1])))
                    self.addToGroup(glasses, "objectsGroup")

                    #Link glasses with the effect so that it can disappear when picked up
                    glasses.attach(occlude)
        
        #Add the effect to the foreground
        self.addToGroup(occlude, "foregroundGroup")

        # GUI elements

        # Register objects to update and event methods
        self.addToGroup([self.player, self.objectsGroup, self.npcGroup], "objectsToUpdate")
        self.addToGroup([self.player], "objectsToEvent")

    def createEnemy(self, enemy):
        data = enemy.split()

        if data[2] == "Basic0":
            basic0 = Basic0([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls())
            self.addToGroup(basic0, "npcGroup")
            self.player.attach(basic0)

        elif data[2] == "Basic1":
            waypoints = [(320, 400), (500, 400)]
            spawn = [int(data[0]), int(data[1])]
            basic1 = Basic1(spawn, self.playerGroup, self.level.getWalls(), waypoints, 0.3)
            self.addToGroup(basic1, "npcGroup")
            self.player.attach(basic1)

        elif data[2] == "Basic12":
            waypoints = [(320, 400), (500, 400)]
            spawn = [int(data[0]), int(data[1])]
            basic12 = Basic1(spawn, self.playerGroup, self.level.getWalls(), waypoints, 0.1)
            self.addToGroup(basic12, "npcGroup")
            self.player.attach(basic12)

        elif data[2] == "Basic2":
            basic2 = Basic2([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls())
            self.addToGroup(basic2, "npcGroup")
            self.player.attach(basic2)

        elif data[2] == "Normal2":
            normal2 = Normal2([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls())
            self.addToGroup(normal2, "npcGroup")
            self.player.attach(normal2)

        elif data[2] == "Advanced2":
            a2 = Advanced2([int(data[0]), int(data[1])], self.playerGroup, self.level.getWalls())
            self.addToGroup(a2, "npcGroup")
            self.player.attach(a2)


    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.wav", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()

    def finish(self):
        scene02 = Scene02Intro()
        Director().change(scene02, fade=True)
