# -*- coding: utf-8 -*-

import json
import os


class MetainfoManager(object):
    """
    Class used to get meta-information of the game (last checkpoint, tutorial passed...)
    """

    ROOT_PATH = ".."  # path of the root of the project
    META_FILE = os.path.join(ROOT_PATH, ".info", "game.json")

    data = None

    @classmethod
    def save(cls):
        """
        Saves the content of self.data into the .JSON file
        """

        if cls.data is None:
            return

        with open(cls.META_FILE, 'w') as file:
            json.dump(cls.data, file, indent=4)
            print("[Metainfo] Changes on the meta file saved")

    @classmethod
    def getInfo(cls):
        """
        Loads, if not already loaded, and returns the configuration from the .JSON configuration file
        """

        # If the data is not loaded
        if cls.data is None:
            # Open and load the content of the file
            with open(cls.META_FILE) as file:
                cls.data = json.load(file)

        return cls.data

    @classmethod
    def getValue(cls, field):
        """
        Returns the value of a specific field
        """

        if cls.data is None:
            cls.getInfo()

        return cls.data[field]

    @classmethod
    def getLastCheckpoint(cls):
        """
        Returns the last scene played
        """
        return cls.getValue("lastCheckpoint")
        
    @classmethod
    def getDeathCounter(cls):
        """
        Returns the number of deaths
        """
        return cls.getValue("deathCounter")

    @classmethod
    def saveCheckpoint(cls, scene):
        """
        Saves the name of the scene as the last checkpoint
        """
        cls.data["lastCheckpoint"] = type(scene).__name__
        cls.save()
    
    @classmethod
    def saveDeathCounter(cls, deathCounter):
        """
        Saves the number of deaths
        """
        cls.data["deathCounter"] = deathCounter
        cls.save()


    @classmethod
    def isTutorialDone(cls):
        """
        Returns True if the player has already done the tutorial
        """
        return cls.getValue("tutorialDone")

    @classmethod
    def setTutorialDone(cls):
        """
        Sets the tutorial done
        """
        cls.data["tutorialDone"] = True
        cls.save()
