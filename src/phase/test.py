# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from effects.occlusion import Occlude
from game.dialogue import Dialogue

from map.level import Level

from phase.phase import Phase

from player.dialogue_character import DialogueCharacter
from player.personaje2 import Player

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

        # Player
        self.player = Player((400, 300))
        self.player.attach(self.level)
        self.addToGroup(self.player, "playerGroup")

        # NPC
        speaker = DialogueCharacter("character2.png", (400,200), self.playerGroup, "avatar.png", "dialg01.txt")
        self.addToGroup(speaker, "npcGroup")

        # Objects
        glasses = Glasses(self.playerGroup, position=(300, 300))
        labcoat = LabCoat(self.playerGroup, position=(600, 400))
        letter = Letter(self.playerGroup, position=(500, 400))
        self.addToGroup([glasses, labcoat, letter], "objectsGroup")

        # Foreground
        occlude = Occlude()
        glasses.attach(occlude)
        self.addToGroup(occlude, "foregroundGroup")

        # GUI elements
        self.dialogue = Dialogue()

        # Register objects to update and event methods
        self.addToGroup([self.player, self.objectsGroup, self.npcGroup], "objectsToUpdate")
        self.addToGroup([letter], "objectsToEvent")

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.ogg", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()

