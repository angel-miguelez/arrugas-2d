# -*- coding: utf-8 -*-

import pygame

from effects.occlusion import Occlude

from map.level import Level

from characters.npc import ElderCharacter, NurseCharacter
from characters.character import Player
from characters.enemy import Basic0, Basic1, Normal2, Basic2, Advanced2
from objects.door import Door, Switch, SwitchOut
from objects.elevator import Elevator

from objects.glasses import Glasses
from objects.labcoat import LabCoat
from objects.letter import Letter
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

        basic0 = Basic0([450, 300], self.playerGroup, self.level.getWalls())
        self.addToGroup(basic0, "npcGroup")
        self.player.attach(basic0)

        waypoints = [(320, 400), (500, 400)]
        spawn = [500, 400]
        basic1 = Basic1(spawn, self.playerGroup, self.level.getWalls(), waypoints)
        self.addToGroup(basic1, "npcGroup")

        basic2 = Basic2([1000, 500], self.playerGroup, self.level.getWalls())
        self.addToGroup(basic2, "npcGroup")
        self.player.attach(basic2)

        #normal2 = Normal2([850, 800], self.playerGroup, self.level.getWalls())
        #self.addToGroup(normal2, "npcGroup")
        #self.player.attach(normal2)

        advanced2 = Advanced2([850, 800], self.playerGroup, self.level.getWalls())
        self.addToGroup(advanced2, "npcGroup")
        self.player.attach(advanced2)

        # Objects
        glasses = Glasses(self.playerGroup, (500, 300))
        labcoat = LabCoat(self.playerGroup, (600, 500))

        #Adding the doors and switches to the scene
        for switch in self.level.getSwitches():
            aux = switch.split()
            data = [int(numeric_string) for numeric_string in aux]
            
            door = Door((data[0], data[1]), self.playerGroup)
            switch = Switch((data[2], data[3]), self.playerGroup)
            if data[4]:
                switch1 = SwitchOut((data[0] - 8, data[1]), self.playerGroup)
            else:
                switch1 = SwitchOut((data[0] + 8, data[1]), self.playerGroup)
                
            letter = Letter(self.playerGroup, (data[5], data[6]), (400, 300))
            switch.attach(door)
            switch.attach(switch1)
            switch1.attach(door)
            letter.attach(door)

            self.addToGroup([letter, door, switch, switch1], "objectsGroup")

        elevator = Elevator(
            self.playerGroup, (self.level.getElevator()[0], self.level.getElevator()[1]))
        self.addToGroup([glasses, labcoat, elevator], "objectsGroup")

        # Foreground
        occlude = Occlude()
        glasses.attach(occlude)
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

    def update(self, *args):
        super().update(*args)
        # print(self.player.lastPos)
