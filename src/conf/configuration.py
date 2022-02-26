# -*- coding: utf-8 -*-

import json
import os
import pygame

from utils.singleton import Singleton


class ConfManager(metaclass=Singleton):
    """
    Class used to retrieve and edit the configuration of the game
    """

    def __init__(self):
        self.CONF_FILE = os.path.join("..", "conf", "configuration.json")
        self.data = None

    def getConf(self):
        """
        Loads, if not already loaded, and returns the configuration from the .JSON configuration file
        """

        # If the data is not loaded
        if self.data is None:

            # Open and load the content of the file
            with open(self.CONF_FILE) as file:
                self.data = json.load(file)

        return self.data

    def getValue(self, key):
        """
        Returns the value of a specific configuration field
        """

        self.data = self.getConf()

        # Iterate over the hierarchy of the key (e.g. player -> movement -> up)
        levels = key.split('.')
        field = self.data[levels[0]]  # root of the field (e.g. player)
        for level in levels[1:]:  # iterate in depth over the hierarchy
            field = field[level]

        return field


    def getBind(self, key, code=True):
        """
        Returns the key name or the key code binded to a specific configuration (key)
        """

        value = self.getValue(key)
        return pygame.key.key_code(value) if code else value  # return the code or the name of the key

    def setBind(self, key, code):
        """
        Edits a specific binding of the configuration
        """

        hierarchy = key.split('.')
        field = hierarchy[-1]  # the field to modify
        path = '.'.join(hierarchy[0:-1])  # the configuration path to the parent of that field

        name = pygame.key.name(code)  # the configuration file uses the name instead of the code of the keys
        self.getValue(path)[field] = name  # get the pointer to the field and modify its value

    def save(self):
        """
        Saves the content of self.data into the .JSON file
        """

        if self.data is None:
            return

        with open(self.CONF_FILE, 'w') as file:
            json.dump(self.data, file, indent=4)
            print("[Configuration] Changes on the configuration file saved")
