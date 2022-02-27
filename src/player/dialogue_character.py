# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from game.dialogue import DynamicDialogueIntervention
from game.director import Director

from objects.interactive import Interactive
from utils.resourcesmanager import ResourcesManager


class DialogueCharacter(Interactive):
    """
    Character whose only behaviour is to speak
    """

    def __init__(self, image, position, playerGroup, avatar, text):
        Interactive.__init__(self, image, [playerGroup], position=position)

        self.player = playerGroup.sprites()[0]

        self.avatar = avatar
        self.text = text

    def onCollisionEnter(self, collided):
        Interactive.onCollisionEnter(self, collided)

        dialogue = Director().getCurrentScene().dialogue
        dialogue.clear()

        interventions = ResourcesManager.loadDialogue(self.text)
        for interv in interventions:
            intervention = DynamicDialogueIntervention()
            intervention.setAvatar(interv[0])
            intervention.setText(interv[1])
            dialogue.add(intervention)

        dialogue.start()
