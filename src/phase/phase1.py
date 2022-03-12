# -*- coding: utf-8 -*-

import pygame

from phase.capture import Capture
from phase.playable import GamePhase

from res.levels import *


class Phase1(GamePhase):
    """
    First playable scene of the game. The player does not know why is he in a residence and tries to escape.
    """

    def __init__(self):
        super().__init__(Capture, basic_layout)

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.wav", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()
