# -*- coding: utf-8 -*-

import random

import pygame

from effects.occlusion import Occlude
from game.director import Director

from map.level import Level

from characters.character import Player

from phase.playable import PlayablePhase

from res.levels import *
from phase.sceneDialog2 import SceneDialog2
from objects.door import Switch


class MoveStartPhase(PlayablePhase):
    """
    Fase usada para probar cosas
    """

    def __init__(self):

        super().__init__()

        # Level
        self.level = Level(moveStartPhase, 400, 300)  # Setup map structure

        # Player
        self.player = Player((400, 300), 0.2)
        self.player.attach(self.level)
        self.player.addCollisionGroup(self.level.getWalls())
        self.addToGroup(self.player, "playerGroup")
        self.level.setPlayer(self.player)

        for idx, switch in enumerate(self.level.getSwitches()):
            aux = switch.split()
            data = [int(numeric_string) for numeric_string in aux]
            switch = Switch("white_tile.jpg", (data[2], data[3]), self.playerGroup, "enter", visible=False)
            if data[4]:
               switch1 = Switch("invisible_tile.png", (data[0] - 50, data[1]), self.playerGroup, "exit", active=False, visible=False)
            else:
                switch1 = Switch("invisible_tile.png", (data[0] + 50, data[1]), self.playerGroup, "exit", active=False, visible=False)

            switch.attach(switch1)
            self.addToGroup([switch], "objectsGroup")

        #Create occlude effect
        occlude = Occlude()

        #Add the effect to the foreground
        self.addToGroup(occlude, "foregroundGroup")

        # Register objects to update and event methods
        self.addToGroup([self.player, self.objectsGroup, self.npcGroup], "objectsToUpdate")
        self.addToGroup([self.player], "objectsToEvent")

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.wav", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()

    def finish(self):
        nextscene = SceneDialog2()
        Director().push(nextscene, fade=True)
