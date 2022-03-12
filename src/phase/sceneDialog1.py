# -*- coding: utf-8 -*-

import pygame

from conf.configuration import ConfManager
from phase.cinematic import DialoguePhase
from phase.sceneDialog2 import SceneDialog2


class SceneDialog1(DialoguePhase):

    def __init__(self):
        super().__init__(SceneDialog2, "intro.jpg", "introduction01.txt")

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
