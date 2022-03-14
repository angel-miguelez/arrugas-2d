# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame.mouse
import pygame_menu
import sys

from game.director import Director
from game.scene import Scene
from pygame_menu import Theme


class Menu(Scene):
    """
    Abstract class which holds the basic attributes and methods of a menu
    """

    def __init__(self, title, **kwargs):

        super().__init__()

        mytheme = pygame_menu.themes.THEME_GREEN.copy()
        myimage = pygame_menu.baseimage.BaseImage(
            image_path='../img/ground.jpg',
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
        )
        mytitle=pygame_menu.widgets.MENUBAR_STYLE_NONE
        mytheme.title_bar_style=mytitle
        mytheme.background_color = myimage
        #mytheme.selection_effect=Theme.widget_selection_effect
        mytheme.widget_font=pygame_menu.font.FONT_MUNRO

        # Every menu has a pygame_menu object
        self._menu = pygame_menu.Menu(title, 800, 600, theme=mytheme, **kwargs)

    def events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # In every menu we can return to the previous menu with K_ESCAPE
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                Director().pop()

        self._menu.update(events)

    def update(self, *args):
        pass

    def draw(self, surface):
        self._menu.draw(surface)

    def onEnterScene(self):
        pygame.mouse.set_visible(True)

    def onExitScene(self):
        pass
