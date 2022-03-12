#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from game.director import Director
from menu.mainmenu import MainMenu


if __name__ == '__main__':

    pygame.init()

    # Create a director and the initial scene (main menu)
    director = Director()
    mainMenu = MainMenu()

    director.push(mainMenu)  # add the main menu as the initial scene
    director.execute()  # start the game loop

    pygame.quit()
