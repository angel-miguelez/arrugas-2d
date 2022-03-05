# -*- coding: utf-8 -*-

from game.dialogue import Dialogue, DynamicDialogueIntervention
from game.director import Director

from phase.cinematic import CinematicPhase
from utils.resourcesmanager import ResourcesManager


class Scene02Intro(CinematicPhase):
    """
    Introduction of the second scene, where the nurses have captured the player
    """

    def __init__(self):

        super().__init__()

        self.backgroundImage = ResourcesManager.loadImage("corridor_background.jpg")

        self.dialogue = Dialogue()

        # Parse the dialogue file and create as many interventions as needed
        interventions = ResourcesManager.loadDialogue("captura.txt")
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
