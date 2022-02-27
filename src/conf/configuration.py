# -*- coding: utf-8 -*-

import json
import os
import pygame


class ConfManager(object):
    """
    Class used to retrieve and edit the configuration of the game
    """

    ROOT_PATH = ".."  # path of the root of the project
    CONF_FILE = os.path.join(ROOT_PATH, "conf", "configuration.json")

    data = None

    @classmethod
    def save(cls):
        """
        Saves the content of self.data into the .JSON file
        """

        if cls.data is None:
            return

        with open(cls.CONF_FILE, 'w') as file:
            json.dump(cls.data, file, indent=4)
            print("[Configuration] Changes on the configuration file saved")

    @classmethod
    def getConf(cls):
        """
        Loads, if not already loaded, and returns the configuration from the .JSON configuration file
        """

        # If the data is not loaded
        if cls.data is None:

            # Open and load the content of the file
            with open(cls.CONF_FILE) as file:
                cls.data = json.load(file)

        return cls.data

    @classmethod
    def getValue(cls, key):
        """
        Returns the value of a specific configuration field
        """

        cls.data = cls.getConf()

        # Iterate over the hierarchy of the key (e.g. player -> movement -> up)
        levels = key.split('.')
        field = cls.data[levels[0]]  # root of the field (e.g. player)
        for level in levels[1:]:  # iterate in depth over the hierarchy
            field = field[level]

        return field

    @classmethod
    def setValue(cls, field, value):
        """
        Edits the value of a specific field of the configuration
        """

        hierarchy = field.split('.')
        field = hierarchy[-1]  # the field to modify
        path = '.'.join(hierarchy[0:-1])  # the configuration path to the parent of that field

        cls.getValue(path)[field] = value  # get the pointer to the field and modify its value

    @classmethod
    def getBind(cls, key, code=True):
        """
        Returns the key name or the key code binded to a specific configuration (key)
        """

        value = cls.getValue(key)
        return pygame.key.key_code(value) if code else value  # return the code or the name of the key

    @classmethod
    def setBind(cls, key, code):
        """
        Edits a specific binding of the configuration
        """

        name = pygame.key.name(code)  # the configuration file uses the name instead of the code of the keys
        cls.setValue(key, name)

    @classmethod
    def getPlayerMovementBinds(cls):
        """
        Wrapper to obtain all the bindings of the player movement
        """

        binds = []
        for bind in ["player.movement.up", "player.movement.down", "player.movement.right", "player.movement.left"]:
            binds.append(cls.getBind(bind))

        return binds
