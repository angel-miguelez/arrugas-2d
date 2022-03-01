# -*- coding: utf-8 -*-

from game.dialogue import DynamicDialogueIntervention, SimpleDialogueIntervention, Dialogue

from objects.object import Interactive
from player.entity import Entity
from utils.resourcesmanager import ResourcesManager


class DialogueCharacter(Entity, Interactive):
    """
    Character whose only behaviour is to speak when the player collides with it
    """

    def __init__(self, image, position, playerGroup, avatar, text):
        Entity.__init__(self, playerGroup.sprites()[0], position)
        Interactive.__init__(self, image, [playerGroup], position=position)

        self.avatar = avatar  # image of the character to display in the dialogue box
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
