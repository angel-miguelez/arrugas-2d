# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from characters.npc import ElderTutorialCharacter, Television, Bed01, Bed02, Mate
from conf.configuration import ConfManager
from conf.metainfo import MetainfoManager
from objects.door import Door
from phase.cinematic import DialoguePhase
from phase.playable import GamePhase
from res.levels import *
from utils.observer import Observer, Subject


class Tutorial(GamePhase, Observer):

    def __init__(self):
        super().__init__(SceneDialog2, 1)

        # Add a door so the player cannot explore the level yet (since it is the same as Phase1)
        door = Door((635, 412), self.playerGroup)
        door._locked = True
        self.objectsGroup.add(door)

        # Partner who explains the player how to move
        self.partner = ElderTutorialCharacter((500, 300), self.playerGroup)
        self.npcGroup.add(self.partner)

        self.movedInDir = [False, False, False, False]  # check that the player know how to move in every direction
        self.lastPos = self.player.lastPos
        self.player.attach(self)

    def update(self, *args):

        # If the player has moved in all directions, finish the tutorial
        if all(self.movedInDir):
            self.finish()

        super().update(*args)

    def onEnterScene(self):
        super().onEnterScene()

        # Provoke a fake collision, to trigger the dialogue
        self.partner.objectsEnterCollision.append(self.player)  # consistency with the collision system
        self.partner.onCollisionEnter(self.player)

    def onExitScene(self):
        super().onExitScene()
        MetainfoManager.setTutorialDone()

    def updateObserver(self, subject: Subject):

        x, y = subject.getPos()

        if y < self.lastPos[1]:
            self.movedInDir[0] = True
        elif y > self.lastPos[1]:
            self.movedInDir[1] = True

        if x < self.lastPos[0]:
            self.movedInDir[2] = True
        elif x > self.lastPos[0]:
            self.movedInDir[3] = True

        self.lastPos = x, y


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
        television = Television((500, 240), self.playerGroup)
        mate = Mate((384, 380), self.playerGroup)
        bed01 = Bed01((400, 540), self.playerGroup)
        bed02 = Bed02((600, 540), self.playerGroup)
        self.npcGroup.add([television, bed01, bed02, mate])

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

