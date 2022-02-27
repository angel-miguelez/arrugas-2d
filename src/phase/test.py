# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys

from effects.occlusion import Occlude
# from game.dialogue import DialogueUI, DynamicDialogueUI
from game.dialogue import Dialogue

from map.level import Level

from phase.phase import Phase

from player.dialogue_character import DialogueCharacter
from player.personaje2 import Player

from objects.glasses import Glasses
from objects.labcoat import LabCoat
from objects.letter import Letter

from res.levels import *
from utils.resourcesmanager import ResourcesManager


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
        self.playerGroup = pygame.sprite.Group(self.player)

        # NPC
        self.speaker = DialogueCharacter("character2.png", (400,200), self.playerGroup, "avatar.png", "dialg01.txt")
        self.npcGroup = pygame.sprite.Group(self.speaker)

        # Objects
        self.glasses = Glasses(self.playerGroup, position=(300, 300))
        self.labcoat = LabCoat(self.playerGroup, position=(600, 400))
        self.letter = Letter(self.playerGroup, position=(500, 400))
        self.objectsGroup = pygame.sprite.Group(self.labcoat, self.letter)

        # Foreground
        self.occlude = Occlude()
        self.glasses.attach(self.occlude)
        self.foregroundGroup = pygame.sprite.Group(self.occlude)

        # GUI elements
        self.dialogue = Dialogue()

        self.uiGroup = [self.dialogue]

        self.objectsToUpdate = [self.player, self.objectsGroup, self.npcGroup, self.dialogue]
        self.objectsToEvent = [self.letter, self.dialogue]


    def events(self, events):

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self._director.pop()

        keys_pressed = pygame.key.get_pressed()
        self.player.move(keys_pressed, self.MOVE_UP, self.MOVE_DOWN, self.MOVE_LEFT, self.MOVE_RIGHT)

        # Cambiar como funciona el player para poder usar esto
        for object in self.objectsToEvent:
            object.events(events)

    def update(self, time):
        for object in self.objectsToUpdate:
            object.update(time)

    def draw(self, surface):
        surface.fill((0, 0, 0))  # Background color

        self.level.run(surface)  # Draw the map

        self.objectsGroup.draw(surface)
        self.playerGroup.draw(surface)
        self.npcGroup.draw(surface)

        self.foregroundGroup.draw(surface)

        for ui in self.uiGroup:
            ui.draw(surface)

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.ogg", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()

