# -*- coding: utf-8 -*-

from phase.cinematic import DialoguePhase
from phase.phase1 import Phase1


class SceneDialog2(DialoguePhase):

    def __init__(self):
        super().__init__(Phase1, "intro.jpg", "introduction02.txt")
