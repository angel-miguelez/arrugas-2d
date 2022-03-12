# -*- coding: utf-8 -*-

import pygame

from conf.configuration import ConfManager
from conf.metainfo import MetainfoManager
from phase.cinematic import DialoguePhase
from phase.playable import GamePhase
from res.levels import *


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

    def onExitScene(self):
        super().onExitScene()
        MetainfoManager.setTutorialDone()


class MoveStartPhase(GamePhase):
    """
    Tutorial to learn how to move the player
    """

    def __init__(self):

        super().__init__(SceneDialog2, moveStartPhase)


class SceneDialog2(DialoguePhase):
    """
    Scene that appears after starting the game from the menu. The partner of Tomas remebers him how it is not the first
    time he tries to escape from the residence
    """
    def __init__(self):
        checkpoint = MetainfoManager.getLastCheckpoint()
        scene = Phase1 if checkpoint is None else eval(MetainfoManager.getLastCheckpoint())
        super().__init__(scene, "intro.jpg", "introduction02.txt")


class Phase1(GamePhase):
    """
    First playable scene of the game. The player does not know why is he in a residence and tries to escape.
    """

    def __init__(self):
        super().__init__(Capture, basic_layout, rooms_1)

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.wav", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()


class Capture(DialoguePhase):
    """
    Introduction of the second scene, where the nurses have captured the player
    """

    def __init__(self):
        super().__init__(Phase2, "corridor_background.jpg", "captura.txt")


class Phase2(GamePhase):
    """
    The player has been captured by the guards, and tries to escape again.
    """

    def __init__(self):
        super().__init__(Phase3, basic_layout_2, rooms_2)

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.wav", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()


class Phase3(GamePhase):
    """
    The player has reached the first floor of the residence, so he reaches the exit he will be free.
    """

    def __init__(self):
        super().__init__(FinalScene, basic_layout_3, rooms_3)

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.wav", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()


class FinalScene(DialoguePhase):
    """
    The end of the game, with the player out of the residence
    """

    def __init__(self):

        super().__init__(None, "city_background.jpg", "huida.txt")

