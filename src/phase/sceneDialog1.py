# -*- coding: utf-8 -*-

from game.dialogue import Dialogue, DynamicDialogueIntervention
from game.director import Director

from phase.cinematic import CinematicPhase
from phase.sceneDialog2 import SceneDialog2
from utils.resourcesmanager import ResourcesManager

from phase.moveStartPhase import MoveStartPhase

class SceneDialog1(CinematicPhase):

    def __init__(self):

        super().__init__()
        self.backgroundImage = ResourcesManager.loadImage("intro.jpg")

        self.dialogue = Dialogue()

        # Parse the dialogue file and create as many interventions as needed
        interventions = ResourcesManager.loadDialogue("introduction01.txt")
        
        for interv in interventions:
            intervention = DynamicDialogueIntervention()
            intervention.setAvatar(interv[0])
            intervention.setText(interv[1])
            self.dialogue.add(intervention)

    def update(self, *args):

        super().update(*args)
        if self.dialogue.finished:
            nextscene = SceneDialog2()#MoveStartPhase()
            Director().push(nextscene, fade=True)
            

    def onEnterScene(self):
        self.dialogue.start()  # start the dialogue
