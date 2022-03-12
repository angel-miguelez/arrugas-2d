# -*- coding: utf-8 -*-


import pygame

from phase.playable import GamePhase
from phase.phase3 import Phase3

from res.levels import *


class Phase2(GamePhase):
    """
    The player has been captured by the guards, and tries to escape again.
    """

    def __init__(self):
        super().__init__(Phase3, basic_layout_2, rooms_2)

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.wav", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()
