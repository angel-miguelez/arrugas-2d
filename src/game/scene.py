# -*- encoding: utf-8 -*-

import pygame

from utils.resourcesmanager import ResourcesManager


class Scene:
    """
    Class that represents a scene of the game, which could be a menu, a game map...
    """

    def __init__(self, director, name):
        self._director = director
        self.name = name

    def events(self, *args):
        """
        Manages pygame events
        """
        raise NotImplemented("event method not implemented.")

    def update(self, *args):
        """
        Updates the scene in base of the events and the current state
        """
        raise NotImplemented("update method not implemented.")

    def draw(self, surface):
        """
        Draws the scene on a surface
        """
        raise NotImplemented("draw method not implemented.")

    def onEnterScene(self):
        """
        Method called right before the scene loop is started by the director
        """
        raise NotImplemented("onEnter method not implemented.")

    def onExitScene(self):
        """
        Method called right after the scene loop is finished by the director
        """
        raise NotImplemented("onExit method not implemented.")

    def playMusic(self, file, volume=1):
        """
        Plays the music file given with a given volume (float or field of configuration file)
        """

        ResourcesManager.loadMusic(file, volume)
        pygame.mixer.music.play(-1)

    def addToGroup(self, object, groupName):
        """
        Adds an object to a specific group, if it exists
        """

        # If the parameter is a list, iterate over it adding each element
        if isinstance(object, list):
            for element in object:
                self.addToGroup(element, groupName)

        # Otherwise, add the element to the list directly
        else:
            group = getattr(self, groupName, None)
            if isinstance(group, list) and object not in group:  # simple lists
                group.append(object)
            elif isinstance(group, pygame.sprite.Group) and object not in group:  # pygame groups
                group.add(object)

    def removeFromGroup(self, object, groupName):
        """
        Removes an object from a specific group, if it exists
        """

        group = getattr(self, groupName, None)
        if group is not None and object in group:
            group.remove(object)
