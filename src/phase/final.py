# -*- coding: utf-8 -*-

from game.dialogue import Dialogue, DynamicDialogueIntervention
from game.director import Director

from phase.cinematic import CinematicPhase
from utils.resourcesmanager import ResourcesManager


class FinalScene(CinematicPhase):
    """
    The end of the game, with the player out of the residence
    """

    def __init__(self):

        super().__init__()

        self.backgroundImage = ResourcesManager.loadImage("city_background.jpg")

        self.dialogue = Dialogue()

        # Parse the dialogue file and create as many interventions as needed
        interventions = ResourcesManager.loadDialogue("huida.txt")
        for interv in interventions:
            intervention = DynamicDialogueIntervention()
            intervention.setAvatar(interv[0])
            intervention.setText(interv[1])
            self.dialogue.add(intervention)

    def update(self, *args):

        super().update(*args)
        if self.dialogue.finished:
            Director().pop(fade=True)

    def onEnterScene(self):
        self.dialogue.start()  # start the dialogue
