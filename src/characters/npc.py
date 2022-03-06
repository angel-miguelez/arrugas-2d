# -*- coding: utf-8 -*-

import random

import pygame

from game.dialogue import DynamicDialogueIntervention, SimpleDialogueIntervention, Dialogue
from objects.object import Interactive
from characters.entity import Entity
from utils.resourcesmanager import ResourcesManager


class DialogueCharacter(pygame.sprite.Sprite, Entity, Interactive):
    """
    Character whose only behaviour is to speak when the characters collides with it
    """

    def __init__(self, image, text, position, playerGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = ResourcesManager.loadImage(image, transparency=True)
        self.rect = self.image.get_rect()
        self.rect.center = position

        Entity.__init__(self)
        Entity.setPlayer(self, playerGroup.sprites()[0], position)

        Interactive.__init__(self, self.rect)
        self.addCollisionGroup(playerGroup)

        self.text = text  # dialogue text file

    def update(self, *args):
        pygame.sprite.Sprite.update(self, *args)
        Interactive.update(self, *args)

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
