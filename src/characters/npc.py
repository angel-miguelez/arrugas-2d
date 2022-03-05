# -*- coding: utf-8 -*-

import random

from game.dialogue import DynamicDialogueIntervention, SimpleDialogueIntervention, Dialogue

from objects.object import Interactive
from characters.entity import Entity
from utils.resourcesmanager import ResourcesManager


class DialogueCharacter(Entity, Interactive):
    """
    Character whose only behaviour is to speak when the characters collides with it
    """

    def __init__(self, image, text, position, playerGroup):
        Entity.__init__(self, playerGroup.sprites()[0], position)
        Interactive.__init__(self, image, [playerGroup], position=position)

        self.text = text  # dialogue text file

    def onCollisionEnter(self, collided):
        Interactive.onCollisionEnter(self, collided)

        dialogue = Dialogue()

        # Parse the dialogue file and create as many interventions as needed
        interventions = ResourcesManager.loadDialogue(self.text)
        for interv in interventions:
            intervention = DynamicDialogueIntervention()
            intervention.setAvatar(interv[0])
            intervention.setText(interv[1])
            dialogue.add(intervention)

        dialogue.start()  # start the dialogue


class ElderCharacter(DialogueCharacter):
    """
    Simple old man character
    """

    def __init__(self, position, playerGroup):

        r = random.randint(1, 8)
        image = f"npc/elder0{r}.png"  # get a random image

        r = random.randint(1, 4)
        dialg = f"elder0{r}.txt"  # get a random dialogue

        DialogueCharacter.__init__(self, image, dialg, position, playerGroup)

class NurseCharacter(DialogueCharacter):
    """
    Simple nurse character
    """

    def __init__(self, position, playerGroup):
        image = "npc/nurse.png"
        dialg = "nurse01.txt"
        DialogueCharacter.__init__(self, image, dialg, position, playerGroup)
