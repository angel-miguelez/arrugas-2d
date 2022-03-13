# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from game.dialogue import TextUI
from game.director import Director

from objects.object import Object

from utils.resourcesmanager import ResourcesManager



class DeathCounter():
    """
    Class that displays the number of player deaths
    """
    
    def __init__(self, deathCounter):
        self.image = ResourcesManager.loadImage("skull.png", transparency=True)
        
        xPos = 550 # calculate the horizontal position of the number in the screen
        yPos = 50
        
        self.rect = self.image.get_rect()
        print(self.rect)
        self.rect.center = (xPos, yPos)
        
        self.ui = TextUI("ds-digi.TTF", 56, (xPos+100, yPos), (255, 255, 255))
        self.ui.setText("x "+str(deathCounter))  # set the text to the number introduced
    
    def draw(self, surface):
        self.ui.draw(surface)
        surface.blit(self.image, self.rect)
        
        
  
