# -*- encoding: utf-8 -*-

import pygame


class Director:
    """
    Class that manages the interaction with the scenes
    """

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self._scenes = []  # list with all the scenes
        self._endScene = False  # if the scene has ended or the user has exited

        self._clock = pygame.time.Clock()

    def loop(self, scene):
        """
        Loop of the current scene
        """

        self._endScene = False

        # Loop of the scene
        while not self._endScene:
            time = self._clock.tick(60)  # 60 FPS

            scene.events(pygame.event.get())  # manage the interaction with the user
            scene.update(time)  # update the state
            scene.draw(self.screen)  # draw on the screen

            pygame.display.flip()

    def execute(self):
        """
        Implements the game loop. It executes the last scene added to the list of scenes, if there is any
        """

        while len(self._scenes) > 0:
            scene = self._scenes[-1]  # get the last scene added
            print("[Director] Executing scene: " + scene.name)

            scene.onEnter()  # configure some settings before the beginning of the scene
            self.loop(scene)  # start the scene
            scene.onExit()  # configure some settings after the end of the scene

    def pop(self):
        """
        Called when we want to finish and remove a scene
        """

        self._endScene = True  # indicate that the current scene is ended in order to finish the scene loop

        if len(self._scenes) > 0:
            scene = self._scenes.pop()  # remove the current scene from the list of scenes
            print("[Director] Removing current scene: " + scene.name)

    def push(self, scene):
        """
        Finishes the current scene and adds a new one to the list of scenes
        """

        self._endScene = True
        self._scenes.append(scene)
        print("[Director] Pushing new scene: " + scene.name)

    def change(self, scene):
        """
        Combines both pop of the current scene and push a new one
        """

        self.pop()
        self.push(scene)


