# -*- encoding: utf-8 -*-

import pygame

from conf.configuration import ConfManager

from utils.singleton import Singleton


class Director(metaclass=Singleton):
    """
    Class that manages the interaction with the scenes
    """

    def __init__(self):

        # Init the window
        pygame.display.set_caption("Arrugas-2D")
        self.screen = pygame.display.set_mode((800, 600))

        # Init the sound system
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()

        # Configure the fps
        self._fps = int(ConfManager().getValue("general.fps"))
        self._clock = pygame.time.Clock()

        self._scenes = []  # list with all the scenes
        self._endScene = False  # if the scene has ended or the user has exited

        self.time = 0  # time since last update, public variable

    def loop(self, scene):
        """
        Loop of the current scene
        """

        self._endScene = False
        pygame.event.clear()  # clean the events triggered before the scene loop

        # Loop of the scene
        while not self._endScene:
            self.time = self._clock.tick(self._fps)

            scene.events(pygame.event.get())  # manage the interaction with the user
            scene.update(self.time)  # update the state
            scene.draw(self.screen)  # draw on the screen

            pygame.display.flip()

    def execute(self):
        """
        Implements the game loop. It executes the last scene added to the list of scenes, if there is any
        """

        while len(self._scenes) > 0:
            scene = self._scenes[-1]  # get the last scene added

            scene.onEnterScene()  # configure some settings before the beginning of the scene
            self.loop(scene)  # start the scene
            scene.onExitScene()  # configure some settings after the end of the scene

    def pop(self):
        """
        Called when we want to finish and remove a scene
        """

        self._endScene = True  # indicate that the current scene is ended in order to finish the scene loop

        if len(self._scenes) > 0:
            self._scenes.pop()  # remove the current scene from the list of scenes

    def push(self, scene):
        """
        Finishes the current scene and adds a new one to the list of scenes
        """

        self._endScene = True
        self._scenes.append(scene)

    def change(self, scene):
        """
        Combines both pop of the current scene and push a new one
        """

        self.pop()
        self.push(scene)

    def getCurrentScene(self):
        """
        Returns the current scene being played
        """

        return self._scenes[-1]
