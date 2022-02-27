# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import os

from conf.configuration import ConfManager


class ResourcesManager(object):
    """
    Class that provides with every kind of resource, such as images or sounds, to the rest of classes.
    It implements the lightweight pattern, so an individual resource is loaded only once (e.g. enemy sprite)
    """

    ROOT_PATH = ".."  # path to the folder which contains all the resources (images, sounds...)
    resources = {}  # map between the name of the resource and the binary itself
            
    @classmethod
    def loadImage(cls, name, colorkey=None, transparency=False):
        """
        Loads an image
        :param colorkey: if the image has no alpha channel, the background with color=colorkey is removed
        :param transparency: True if the image has an alpha channel
        """

        # If the image has been already loaded, return it directly
        if name in cls.resources:
            return cls.resources[name]

        # Otherwise, load it from the image folder
        fullname = os.path.join(cls.ROOT_PATH, "img", name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print('Cannot load image:', fullname)
            raise SystemExit

        # Convert the image
        if transparency:
            image = image.convert_alpha()

        # If it has not an alpha channel, get the color key to remove the background fill
        else:
            image = image.convert()

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))

                image.set_colorkey(colorkey, RLEACCEL)

        cls.resources[name] = image  # save it in the map of resources

        return image

    @classmethod
    def loadCoordFile(cls, name):
        """
        Loads the content of a file with coordinates
        """

        # If the image has been already loaded, return it directly
        if name in cls.resources:
            return cls.resources[name]

        # Otherwise, load it, read the content and save it in the map of resources
        fullname = os.path.join(cls.ROOT_PATH, 'img', name)

        pfile = open(fullname, 'r')
        data = pfile.read()
        pfile.close()

        cls.resources[name] = data

        return data

    @classmethod
    def loadSound(cls, name):
        """
        Loads a sound effect
        """

        # If the sound has been already loaded, return it directly
        if name in cls.resources:
            return cls.resources[name]

        # Otherwise, load it, and save it in the map of resources
        fullname = os.path.join(cls.ROOT_PATH, "sound", name)
        try:
            sound = pygame.mixer.Sound(fullname)
            sound.set_volume(ConfManager.getValue("sound.sound_effects_volume"))
            cls.resources[name] = sound
            return sound
        except pygame.error:
            print('Cannot load sound:', fullname)
            raise SystemExit

    @classmethod
    def loadMusic(cls, filename, volume=None):
        """
        Loads a music file. This is diferent to loadSound because pygame does not return an object with the music so
        it cannot be saved to reuse.
        """

        fullname = os.path.join(cls.ROOT_PATH, "sound", filename)
        try:
            # Since mixer.music.load does not return anything, we cannot save it in the map or resources
            pygame.mixer.music.load(fullname)

            # If a non-numerical volume value was given, read it from the configuration file
            if not isinstance(volume, float):
                volume = float(ConfManager.getValue(volume))
            pygame.mixer.music.set_volume(volume)

            return True

        except pygame.error:
            print('Cannot load music:', fullname)
            raise SystemExit

    @classmethod
    def loadFont(cls, name, size=0):
        """
        Loads a font
        """

        id = name + str(size)  # since the same family font with different sizes are different objects

        # If the font has been already loaded, return it directly
        if id in cls.resources:
            return cls.resources[id]

        # Otherwise, load it, and save it in the map of resources
        fullname = os.path.join(cls.ROOT_PATH, "font", name)
        try:
            font = pygame.font.SysFont(fullname, size)
            cls.resources[id] = font
            return font
        except pygame.error:
            print('Cannot load font:', fullname)
            raise SystemExit

    @classmethod
    def loadDialogue(cls, name):
        """
        Loads the avatar and text of each player in a dialogue
        """

        # If the dialogue has been already loaded, return it directly
        if id in cls.resources:
            return cls.resources[id]

        # Otherwise, load it, and save it in the map of resources
        fullname = os.path.join(cls.ROOT_PATH, "dialogue", name)
        try:
            pfile = open(fullname, 'r', encoding='utf-8')
            data = pfile.read()
            pfile.close()

            out = []
            interventions = data.split('@')[1:]  # each character interventions starts with @<avatar_file>.png

            for intervention in interventions:
                tmp = intervention.split('\n')

                avatar = tmp[0]  # the avatar is the first line of the intervention
                text = '\n'.join(tmp[1:])

                # paragraphs are separate by a '#', and each line by a '\n'
                # so we create a list (paragraphs) of lists (lines)
                paragraphs = [paragraph.strip('\n').split('\n') for paragraph in text.split('#')]
                out.append((avatar, paragraphs))

            cls.resources[id] = out
            return out

        except pygame.error:
            print('Cannot load font:', fullname)
            raise SystemExit
