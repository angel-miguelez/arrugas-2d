# -*- coding: utf-8 -*-

from phase.cinematic import DialoguePhase


class FinalScene(DialoguePhase):
    """
    The end of the game, with the player out of the residence
    """

    def __init__(self):

        super().__init__(None, "city_background.jpg", "huida.txt")
