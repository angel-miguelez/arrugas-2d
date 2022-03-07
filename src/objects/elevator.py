# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from game.dialogue import TextUI
from game.director import Director

from objects.object import Object

from utils.resourcesmanager import ResourcesManager


class CodeLock(pygame.sprite.Sprite):
    """
    Object that displays an input of 4 numbers that must be filled according to its password
    """

    def __init__(self, password):
        pygame.sprite.Sprite.__init__(self)

        # Load the sprite common fields
        self.image = ResourcesManager.loadImage("code_lock.png", transparency=True)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)

        self.password = password
        self.numbers = []  # TextUI elements
        self.input = []  # numbers introduced

    def clear(self):
        """
        Clears the 4 fields of the input
        """

        self.input = []

        for number in self.numbers:
            Director().getCurrentScene().removeFromGroup(number, "uiGroup")
        self.numbers = []

    def close(self):
        """
        Removes the object from the scene (display)
        """

        self.clear()
        Director().getCurrentScene().removeFromGroup(self, "foregroundGroup")

    def addNumber(self, number):
        """
        Introduces the next number in the sequence of numbers
        """

        self.input.append(number)

        xPos = (len(self.input) - 1) * 170 + 100  # calculate the horizontal position of the number in the screen
        ui = TextUI("ds-digi.ttf", 180, (xPos, 200), (0, 0, 0))
        ui.setText(str(number))  # set the text to the number introduced
        self.numbers.append(ui)

        Director().getCurrentScene().addToGroup(ui, "uiGroup")  # add the UI object to the scene
        ResourcesManager.loadSound("beep.wav").play()

    def enterPassword(self):
        """
        Checks if the input and the real password are the same. If so, returns True, otherwise False
        """

        for idx in range(0, 4):
            if self.password[idx] != self.input[idx]:  # one number mismatched
                ResourcesManager.loadSound("wrong_password.wav").play()
                self.clear()  # reset the input to try again
                return False

        ResourcesManager.loadSound("correct_password.wav").play()
        return True


class Elevator(Object):
    """
    Object which allows the player to continue to the next scene. For that, the player must enter the correct code to
    unlock the elevator
    """

    def __init__(self, password, playerGroup, position):
        super().__init__("elevator.png", position, playerGroup)

        self.password = password  # random number between 0000-9999
        self.codeLock = CodeLock(password)
        print("Password: ", password)

    def onCollisionEnter(self, collided):
        scene = Director().getCurrentScene()
        scene.pauseEvents()  # so the player has to enter the code before moving again
        scene.addToGroup(self, "objectsToEvent")  # to enter the password
        scene.addToGroup(self.codeLock, "foregroundGroup")  # display the current input

    def close(self):
        """
        Closes the code lock input and returns the events to the player
        """

        self.codeLock.close()
        scene = Director().getCurrentScene()
        scene.removeFromGroup(self, "objectsToEvents")
        scene.unpauseEvents()

    def events(self, events):

        for event in events:

            if event.type == KEYDOWN:

                if event.key == K_RETURN:  # return to the game
                    self.close()

                elif K_0 <= event.key <= K_9:  # only numbers between 0-9
                    self.codeLock.addNumber(int(event.key - K_0))  # add the number to the list of inputs

                    if len(self.codeLock.input) == 4:  # if we have filled all the 4 numbers
                        if self.codeLock.enterPassword():  # if the password was correct, go the next scene
                            Director().getCurrentScene().finish()
                        else:  # otherwise, clear the password input to try again
                            self.codeLock.clear()
