# -*- coding: utf-8 -*-

import pygame

from characters.npc import ElderTutorialCharacter
from conf.metainfo import MetainfoManager
from objects.door import Switch
from phase.cinematic import DialoguePhase
from phase.playable import GamePhase
from utils.observer import Observer, Subject


class Tutorial(GamePhase, Observer):

    def __init__(self):
        super().__init__(SceneDialog2, 0)

        switch = Switch("switch.png", (500, 500), self.playerGroup, [])
        switch.attach(self)
        self.npcGroup.add(switch)

        # Partner who explains the player how to move
        self.partner = ElderTutorialCharacter((500, 300), self.playerGroup)
        self.npcGroup.add(self.partner)

    def onEnterScene(self):
        super().onEnterScene()

        # Provoke a fake collision, to trigger the dialogue
        self.partner.objectsEnterCollision.append(self.player)  # consistency with the collision system
        self.partner.onCollisionEnter(self.player)

    def onExitScene(self):
        super().onExitScene()
        MetainfoManager.setTutorialDone()

    def updateObserver(self, subject: Subject):
        self.finish()


class SceneDialog2(DialoguePhase):
    """
    Scene that appears after starting the game from the menu. The partner of Tomas remembers him how it is not the first
    time he tries to escape from the residence
    """

    def __init__(self):
        checkpoint = MetainfoManager.getLastCheckpoint()

        # Sanity check, because if no checkpoint is available, the menu would have loaded the Tutorial
        if checkpoint is None:
            checkpoint = "Tutorial"

        # If the tutorial has been done, load Phase1
        elif checkpoint == "Tutorial":
            checkpoint = "Phase1"

        super().__init__(eval(checkpoint), "intro.jpg", "introduction02.txt")


class Phase1(GamePhase):
    """
    First playable scene of the game. The player does not know why is he in a residence and tries to escape.
    """

    def __init__(self):
        super().__init__(Capture, 1)

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
        super().__init__(Phase3, 2)

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
        super().__init__(FinalScene, 3)

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

