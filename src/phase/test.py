# -*- coding: utf-8 -*-

from tokenize import String
import pygame
from pygame.locals import *

from effects.occlusion import Occlude

from map.level import Level

from characters.npc import DialogueCharacter, ElderCharacter, NurseCharacter
from characters.personaje2 import Player, Basic0, Basic1, Normal2, Basic2, Advanced2
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
        #self.level = Level(basic_layout_2, 400, 300)  # Setup map structure

        # Player
        self.player = Player((400, 300), 0.3)
        self.player.attach(self.level)
        self.player.addCollisionGroup(self.level.walls)
        self.addToGroup(self.player, "playerGroup")
        self.level.setPlayer(self.player)

        # NPC
        speaker = ElderCharacter((800, 400), self.playerGroup)
        nurse = NurseCharacter((800, 600), self.playerGroup)
        self.addToGroup([speaker, nurse], "npcGroup")

        # Enemies
        # for enemyGroup in self.level.enemies:
        #     if enemyGroup == []:
        #         pass
        #     else:
        #         for enemy in enemyGroup:
        #             self.createEnemy(enemy)

        #basic0 = Basic0([300, 300])
        #self.addToGroup(basic0, "npcGroup")
        basic0 = Basic0([450, 300], self.playerGroup, self.level.walls)
        self.addToGroup(basic0, "npcGroup")
        basic0.setPlayer(self.player, (450, 300))
        self.player.attach(basic0)

        waypoints = [(320, 400), (500, 400)]
        spawn = [500, 400]
        basic1 = Basic1(spawn, waypoints, 0.3, self.playerGroup, self.level.walls)
        self.addToGroup(basic1, "npcGroup")

        basic2 = Basic2([1000, 500], 200, self.playerGroup, self.level.walls)
        self.addToGroup(basic2, "npcGroup")
        basic2.setPlayer(self.player, (1000, 500))
        self.player.attach(basic2)

        # normal2 = Normal2([500, 300], self.playerGroup, self.level.walls)
        # self.addToGroup(normal2, "npcGroup")
        # normal2.setPlayer(self.player, (850, 400))
        # self.player.attach(normal2)

        advanced2 = Advanced2([850, 800], self.playerGroup, self.level.walls, "LEFT")
        self.addToGroup(advanced2, "npcGroup")
        advanced2.setPlayer(self.player, (850, 800))
        self.player.attach(advanced2)

        # Objects
        glasses = Glasses(self.playerGroup, (500, 300))
        labcoat = LabCoat(self.playerGroup, (600, 500))
        letter = Letter(self.playerGroup, (1100, 412), (400, 300))

        door = Door((953, 412), self.playerGroup)
        switch = Switch((1003, 412), self.playerGroup)
        switch1 = SwitchOut((940, 412), self.playerGroup)
        switch.attach(door)
        switch.attach(switch1)
        switch1.attach(door)
        letter.attach(door)

        elevator = Elevator(self.playerGroup, (1018, 2021))
        self.addToGroup([glasses, labcoat, letter, door, switch, switch1, elevator], "objectsGroup")

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
            basic0 = Basic0([int(data[0]), int(data[1])], self.playerGroup, self.level.walls)
            self.addToGroup(basic0, "npcGroup")
            basic0.setPlayer(self.player, (int(data[0]), int(data[1])))
            self.player.attach(basic0)

        elif data[2] == "Basic1":
            waypoints = [(320, 400), (500, 400)]
            spawn = [int(data[0]), int(data[1])]
            #spawn = [500, 500]
            basic1 = Basic1(spawn, waypoints, 0.3, self.playerGroup, self.level.walls)
            self.addToGroup(basic1, "npcGroup")
            basic1.setPlayer(self.player, (int(data[0]), int(data[1])))
            self.player.attach(basic1)

        elif data[2] == "Basic2":
            basic2 = Basic2([int(data[0]), int(data[1])],
                            500, self.playerGroup, self.level.walls)
            #basic2 = Basic2([400, 400], self.player, 500, self.playerGroup)
            self.addToGroup(basic2, "npcGroup")
            basic2.setPlayer(self.player, (int(data[0]), int(data[1])))
            self.player.attach(basic2)

        elif data[2] == "Normal2":
            normal2 = Normal2([int(data[0]), int(data[1])], self.playerGroup, self.level.walls)
            self.addToGroup(normal2, "npcGroup")
            normal2.setPlayer(self.player, (int(data[0]), int(data[1])))
            self.player.attach(normal2)

        elif data[2] == "Advanced2":
            a2 = Advanced2([int(data[0]), int(data[1])], 0.2, self.playerGroup, self.level.walls, "LEFT")
            self.addToGroup(a2, "npcGroup")
            a2.setPlayer(self.player, (int(data[0]), int(data[1])))
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
