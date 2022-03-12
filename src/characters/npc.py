# -*- coding: utf-8 -*-

import random

import pygame

from conf.configuration import ConfManager
from game.dialogue import DynamicDialogueIntervention, SimpleDialogueIntervention, Dialogue
from objects.object import Interactive
from characters.entity import Entity
from utils.resourcesmanager import ResourcesManager


class DialogueCharacter(pygame.sprite.Sprite, Entity, Interactive):
    """
    Character whose only behaviour is to speak when the characters collide with it
    """

    def __init__(self, image, text, position, playerGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = ResourcesManager.loadImage(image, transparency=True)
        self.rect = self.image.get_rect()
        self.rect.center = position

        Entity.__init__(self, position)
        Entity.setPlayer(self, playerGroup.sprites()[0])

        Interactive.__init__(self, self.rect)
        self.addCollisionGroup(playerGroup)

        self.text = text  # dialogue text file
        self.dialogue = None

    def update(self, *args):
        pygame.sprite.Sprite.update(self, *args)
        Interactive.updateCollisions(self, *args)

    def onCollisionEnter(self, collided):
        Interactive.onCollisionEnter(self, collided)

        collided.x, collided.y = collided.lastPos
        self.objectsEnterCollision.remove(collided)  # so if still moves to the same direction we can get it again

        self.dialogue = Dialogue()

        # Parse the dialogue file and create as many interventions as needed
        interventions = ResourcesManager.loadDialogue(self.text)
        for interv in interventions:
            intervention = DynamicDialogueIntervention()
            intervention.setAvatar(interv[0])
            intervention.setText(interv[1])
            self.dialogue.add(intervention)

        self.dialogue.start()  # start the dialogue


class ElderCharacter(DialogueCharacter):
    """
    Simple old man character
    """

    def __init__(self, position, playerGroup, dialogue=None):

        r = random.randint(1, 8)
        image = f"npc/elder0{r}.png"  # get a random image

        if dialogue is None:
            r = random.randint(1, 4)
            dialg = f"elder0{r}.txt"  # get a random dialogue
        else:
            dialg = dialogue

        DialogueCharacter.__init__(self, image, dialg, position, playerGroup)


class ElderTutorialCharacter(ElderCharacter):
    """
    Elder character whose text explains the player how to move
    """

    def __init__(self, position, playerGroup):

        r = random.randint(1, 8)
        image = f"npc/elder0{r}.png"  # get a random image

        DialogueCharacter.__init__(self, image, "introduction01.txt", position, playerGroup)

    def onCollisionEnter(self, collided):
        super().onCollisionEnter(collided)

        # Update the text to put the player movement bindings in the tutorial text
        paragraphWithKeys = self.dialogue.interventions[-1].text[-1]
        playerBindings = [pygame.key.name(code) for code in ConfManager.getPlayerMovementBinds()]

        for idx, line in enumerate(paragraphWithKeys):
            line = line.replace("UP", f"[{playerBindings[0]}]")
            line = line.replace("LEFT", f"[{playerBindings[3]}]")
            line = line.replace("DOWN", f"[{playerBindings[1]}]")
            line = line.replace("RIGHT", f"[{playerBindings[2]}]")
            paragraphWithKeys[idx] = line

        self.dialogue.interventions[-1].text[-1] = paragraphWithKeys


class NurseCharacter(DialogueCharacter):
    """
    Simple nurse character
    """

    def __init__(self, position, playerGroup):
        image = "npc/nurse.png"
        dialg = "nurse01.txt"
        DialogueCharacter.__init__(self, image, dialg, position, playerGroup)
