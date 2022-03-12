# -*- coding: utf-8 -*-

import pygame

from phase.playable import GamePhase
from phase.final import FinalScene

from res.levels import *


class Phase3(GamePhase):
    """
    The player has reached the first floor of the residence, so he reaches the exit he will be free.
    """

    def __init__(self):
        super().__init__(FinalScene, basic_layout_3, rooms_3)

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.wav", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()

