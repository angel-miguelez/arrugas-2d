# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from effects.occlusion import Occlude

from map.level import Level

from phase.phase import Phase

from characters.npc import DialogueCharacter, ElderCharacter, NurseCharacter
from characters.personaje2 import Player, Basic0, Basic1, Normal2, Basic2

from objects.glasses import Glasses
from objects.labcoat import LabCoat
from objects.letter import Letter

from res.levels import *


class PhaseTest(Phase):
    """
    Fase usada para probar cosas
    """

    def __init__(self, director):
        super().__init__(director, "PhaseTest")

        # Level
        self.level = Level(basic_layout, 400, 300)  # Setup map structure
        #self.level = Level(basic_layout_2, 400, 300)  # Setup map structure

        # Player
        self.player = Player((400, 300), 0.2)
        self.player.attach(self.level)
        self.player.addCollisionGroup(self.level.walls)
        self.addToGroup(self.player, "playerGroup")
        self.level.setPlayer(self.player)

        # NPC
        speaker = ElderCharacter((800, 400), self.playerGroup)
        nurse = NurseCharacter((800, 600), self.playerGroup)
        self.addToGroup([speaker, nurse], "npcGroup")

        # Enemies
        for enemyGroup in self.level.enemies:
            for enemy in enemyGroup:
                self.addToGroup(enemy, "npcGroup")
                self.player.attach(enemy)

        #basic0 = Basic0([300, 300])
        #self.addToGroup(basic0, "npcGroup")
        basic0 = Basic0([300, 300])
        self.addToGroup(basic0, "npcGroup")
        basic0.setPlayer(self.player, (300, 300))
        self.player.attach(basic0)

        #waypoints = [(360, 200), (140, 200)]
        #spawn = [140, 200]
        #basic1 = Basic1(spawn, waypoints, 1.5)
        #self.addToGroup(basic1, "npcGroup")

        #basic2 = Basic2([500, 500], self.player, 500)
        #self.addToGroup(basic2, "npcGroup")

        #normal2 = Normal2([500, 300], self.player)
        #self.addToGroup(normal2, "npcGroup")

        # Objects
        glasses = Glasses(self.playerGroup, (400, 300))
        labcoat = LabCoat(self.playerGroup, (600, 500))
        letter = Letter(self.playerGroup, (500, 400), (400, 300))
        self.addToGroup([glasses, labcoat, letter], "objectsGroup")

        # Foreground
        occlude = Occlude()
        glasses.attach(occlude)
        self.addToGroup(occlude, "foregroundGroup")

        # GUI elements

        # Register objects to update and event methods
        self.addToGroup([self.player, self.objectsGroup, self.npcGroup], "objectsToUpdate")
        self.addToGroup([self.player, letter], "objectsToEvent")

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.ogg", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()

