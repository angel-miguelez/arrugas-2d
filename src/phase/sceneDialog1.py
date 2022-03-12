# -*- coding: utf-8 -*-

from phase.cinematic import DialoguePhase
from phase.sceneDialog2 import SceneDialog2


class SceneDialog1(DialoguePhase):

    def __init__(self):
        super().__init__(SceneDialog2, "intro.jpg", "introduction01.txt")
