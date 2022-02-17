# -*- encoding: utf-8 -*-


class Scene:
    """
    Class that represents a scene of the game, which could be a menu, a game level...
    """

    def __init__(self, director, name):
        self._director = director
        self.name = name

    def events(self, *args):
        """
        Method that manages pygame events
        """
        raise NotImplemented("event method not implemented.")

    def update(self, *args):
        """
        Method to update the scene in base of the events and the current state
        """
        raise NotImplemented("update method not implemented.")

    def draw(self, surface):
        """
        Method to draw the scene on a surface
        """
        raise NotImplemented("draw method not implemented.")

    def onEnter(self):
        """
        Method called right before the scene loop is started by the director
        """
        raise NotImplemented("onEnter method not implemented.")

    def onExit(self):
        """
        Method called right after the scene loop is finished by the director
        """
        raise NotImplemented("onExit method not implemented.")
