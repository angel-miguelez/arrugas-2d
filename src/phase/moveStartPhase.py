# -*- coding: utf-8 -*-

import pygame

from game.director import Director
from map.level import Level
from characters.character import Player

from phase.playable import GamePhase

from res.levels import *
from phase.sceneDialog2 import SceneDialog2


class MoveStartPhase(GamePhase):
    """
    Tutorial to learn how to move the player
    """

    def __init__(self):

        super().__init__(SceneDialog2, moveStartPhase)


