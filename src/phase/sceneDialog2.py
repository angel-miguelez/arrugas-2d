# -*- coding: utf-8 -*-

from game.dialogue import Dialogue, DynamicDialogueIntervention
from game.director import Director

from phase.cinematic import CinematicPhase
from utils.resourcesmanager import ResourcesManager

from phase.phase1 import Phase1

class SceneDialog2(CinematicPhase):

    def __init__(self):

        super().__init__()
        self.backgroundImage = ResourcesManager.loadImage("intro.jpg")

        self.dialogue = Dialogue()

        # Parse the dialogue file and create as many interventions as needed
        interventions = ResourcesManager.loadDialogue("introduction02.txt")
        
        for interv in interventions:
            intervention = DynamicDialogueIntervention()
            intervention.setAvatar(interv[0])
            intervention.setText(interv[1])
            self.dialogue.add(intervention)

    def update(self, *args):

        super().update(*args)
        if self.dialogue.finished:
            nextscene = Phase1()
            Director().push(nextscene, fade=True)
            

    def onEnterScene(self):
        self.dialogue.start()  # start the dialogue
