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
        self._HEIGHT, self._WIDTH = (800, 600)
        self.screen = pygame.display.set_mode((self._HEIGHT, self._WIDTH))

        # Init the sound system
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()

        # Configure the fps
        self._fps = int(ConfManager().getValue("general.fps"))
        self._clock = pygame.time.Clock()

        self._scenes = []  # list with all the scenes
        self._endScene = False  # if the scene has ended or the user has exited

        self._transitioning = False  # if there is being a transition to the next scene
        self._transitionDuration = 1000  # ms
        self._transitionCounter = 0  # time that the transition has being active

        self.time = 0  # time since last update, public variable

    def _fadeOut(self, time, surface):
        """
        Draws a transparent surface on the surface. It makes an effect from lighter to darker, so the surface is
        completely normal (scene.draw) when starting the effect and completely black at the end.
        """

        # Create a transparent surface of the same size of the window
        transparentSurface = pygame.Surface((self._HEIGHT, self._WIDTH), pygame.SRCALPHA)
        alphaValue = int(self._transitionCounter / self._transitionDuration*255)  # increment opacity with time (0-255)

        transparentSurface.fill((0, 0, 0, alphaValue))  # fill the transparent surface with a black color
        surface.blit(transparentSurface, (0, 0))  # draw on the surface

        # Update the time and check if the effect, and the scene, must end
        self._transitionCounter += time
        if len(self._scenes) > 0 and self._transitionCounter >= self._transitionDuration:
            self._endScene = True  # indicate that the current scene is ended in order to finish the scene loop
            self._transitioning = False
            self._transitionCounter = 0
            self._scenes.pop()  # remove the current scene from the list of scenes

    def loop(self, scene):
        """
        Loop of the current scene
        """

        self._endScene = False
        pygame.event.clear()  # clean the events triggered before the scene loop

        # Loop of the scene
        while not self._endScene:
            self.time = self._clock.tick(self._fps)

            if not self._transitioning:  # normal behaviour
                scene.events(pygame.event.get())  # manage the interaction with the user
                scene.update(self.time)  # update the state

            scene.draw(self.screen)  # draw on the screen

            if self._transitioning:  # start the transition effect
                self._fadeOut(self.time, self.screen)

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

    def pop(self, fade=False):
        """
        Called when we want to finish and remove a scene
        """

        if fade:
            self._transitioning = True  # start the fade out
            # We do not remove the scene since we want a smooth transition, so it is removed at the end of it
        else:
            self._endScene = True
            self._scenes.pop()

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
