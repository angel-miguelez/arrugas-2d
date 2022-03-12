# -*- coding: utf-8 -*-

from phase.cinematic import DialoguePhase
from phase.phase2 import Phase2


class Capture(DialoguePhase):
    """
    Introduction of the second scene, where the nurses have captured the player
    """

    def __init__(self):

        super().__init__(Phase2, "corridor_background.jpg", "captura.txt")
