#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from game.director import Director
from menu.menu import *

# Execute it as a module from arrugas-2d/src directory: python -m  main
if __name__ == '__main__':

    pygame.init()

    # Create a director and the initial scene
    director = Director()
    mainMenu = MainMenu(director)

    director.push(mainMenu)  # add the main menu as the initial scene
    director.execute()  # start the game loop

    pygame.quit()
