# -*- coding: utf-8 -*-

import pygame

import json
import os

from utils.Singleton import Singleton


class ConfManager(metaclass=Singleton):
    """
    Class used to retrieve and edit the configuration of the game
    """

    def __init__(self):
        self.CONF_FILE = os.path.join("..", "conf", "configuration.json")
        self.data = None

    def getConf(self):
        """
        Method to load, if not already loaded, and return the configuration from the .JSON configuration file
        """

        # If the data is not loaded
        if self.data is None:

            # Open and load the content of the file
            with open(self.CONF_FILE) as file:
                self.data = json.load(file)

        return self.data

    def getBind(self, key, code=True):
        """
        Returns the key name or the key code binded to a specific configuration (key)
        """

        self.data = self.getConf()

        # Iterate over the hierarchy of the key (e.g. player -> movement -> up)
        levels = key.split('.')
        field = self.data[levels[0]]  # root level (e.g. player)
        for level in levels[1:]:  # iterate in depth (player[movement] --> player[movement][up]
            field = field[level]

        return pygame.key.key_code(field) if code else field  # return the code or the name of the key

    def setBind(self, key, code):
        """
        Edits a specific binding of the configuration
        """

        self.data = self.getConf()
        name = pygame.key.name(code)  # the configuration file uses the name instead of the code of the keys

        # Iterate over the hierarchy of the key (e.g. player -> movement -> up)
        levels = key.split('.')
        field = self.data[levels[0]]  # root level (e.g. player)
        for level in levels[1:-1]:  # iterate in depth until the last field (the one whose value is edited)
            field = field[level]

        field[levels[-1]] = name  # edit the value of the field

    def save(self):
        """
        Saves the content of self.data into the .JSON file
        """

        if self.data is None:
            return

        with open(self.CONF_FILE, 'w') as file:
            json.dump(self.data, file, indent=4)
            print("[Configuration] Changes on the configuration file saved")
