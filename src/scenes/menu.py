# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame.mouse
import pygame_menu
import sys

from conf.configuration import ConfManager
from conf.metainfo import MetainfoManager
from game.director import Director
from scenes.history import SceneDialog2, Tutorial
from scenes.scene import Scene


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


backgroundColorText = (118, 118, 118)
font_shad_color = (0, 0, 0)
sel_color = (255, 255, 255)


class MainMenu(Menu):
    """
    Class which holds the main menu of the game
    """

    def __init__(self):
        super().__init__("")

        self._menu.add.button('Empezar', self.onStartGame, button_id="start", font_color=backgroundColorText,
                              font_shadow=True, font_shadow_offset=1, font_shadow_color=font_shad_color,
                              selection_color=sel_color)  # button to start the game
        settingsSubMenu = SettingsMenu(self._menu.get_theme())
        self._menu.add.button('Ajustes', SettingsMenu(self._menu.get_theme())._menu, font_color=backgroundColorText,
                              font_shadow=True, font_shadow_offset=1, font_shadow_color=font_shad_color,
                              selection_color=sel_color)  # button to edit the configuration
        self._menu.add.button('Salir', pygame_menu.events.EXIT, font_color=backgroundColorText,
                              font_shadow=True, font_shadow_offset=1, font_shadow_color=font_shad_color,
                              selection_color=sel_color)  # button to exit the game

        self._startGame = False  # flag to know when to stop the main menu music
        self.playMusic("main_menu2.wav", "sound.menu_music_volume")

    def onEnterScene(self):
        super().onEnterScene()

        tutorialDone = MetainfoManager.isTutorialDone()
        startButton = self._menu.get_widget("start")
        startButton.set_title("Continuar" if tutorialDone else 'Empezar')

        # If the player returns from the game, instead from a submenu, set again the menu music
        if self._startGame:
            self._startGame = False
            self.playMusic("main_menu2.wav", "sound.menu_music_volume")

    def onExitScene(self):
        super().onExitScene()

        if self._startGame:
            pygame.mixer.music.stop()

    def onStartGame(self):
        """
        Initiate the game
        """

        self.playMusic("button2.wav", "sound.menu_music_volume")
        self._startGame = True
        Director().push(SceneDialog2() if MetainfoManager.isTutorialDone() else Tutorial(), fade=True)


class SettingsMenu:
    """
    Class which holds the configuration submenu and allows the user to edit it
    """

    def __init__(self, theme):

        myimage = pygame_menu.baseimage.BaseImage(
            image_path='../img/ground2.jpg',
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
        )

        self._conf = ConfManager()  # get the instance of the ConfManager

        self._bindings = {}  # mapping from the configuration field name to its value e.g. {"player.movement.up" : "w"}
        self._dynamicButtonsBinds = {}  # mapping from the configuration field name to the button object
        self._dynamicButtonsTitle = {}  # mapping from the configuration field name to the button title

        theme.background_color = myimage

        self._menu = pygame_menu.Menu(" ", 800, 600, theme=theme)
        self._loadPlayerMovementBindings()  # load the player movement bindings and create buttons to edit them
        self._menu.add.vertical_margin(30)
        self._loadVolumeSettings()  # load the music and sound effects volumes and create buttons to edit them
        self._menu.add.vertical_margin(30)
        self.returnButton = self._menu.add.button('Volver', self.saveAndReturn, self._menu, self._conf,
                                                  font_color=backgroundColorText,
                                                  font_shadow=True, font_shadow_offset=1,
                                                  font_shadow_color=font_shad_color,
                                                  selection_color=sel_color)  # button to return to the main menu

    def saveAndReturn(self, menu, conf):
        conf.save()
        menu.reset(1)

    def _editBinding(self, fieldName):
        """
        Edits the binding with name 'fieldName'. Notice that the configuration is saved after
        the menu is left.
        """

        assigned = False  # flag to indicate that the user has assigned a key to the binding

        while not assigned:  # wait until the user assigns a key
            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # If the user decides to go back to the main menu
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    Director().pop()
                    return

                # If the user presses a key, then it is assigned
                elif event.type == KEYDOWN:

                    # Get the code and the name of the key
                    keyCode = event.key
                    keyName = pygame.key.name(keyCode)

                    # Update the text of the button
                    text = f"{self._dynamicButtonsTitle[fieldName]}'{keyName}'"
                    self._dynamicButtonsBinds[fieldName].set_title(text)

                    # Update the configuration
                    self._conf.setBind(fieldName, keyCode)

                    assigned = True  # exit the loop

    def _loadPlayerMovementBindings(self):
        """
        Loads the player movement bindings and creates a button to edit each of them
        """

        for bind in ["up", "down", "right", "left"]:
            fieldName = "player.movement." + bind
            keyName = self._conf.getBind(fieldName, code=False)

            self._bindings[f"{fieldName}"] = keyName

            if bind == "up":
                movimiento = "arriba"
            elif bind == "down":
                movimiento = "abajo"
            elif bind == "right":
                movimiento = "derecha"
            else:
                movimiento = "izquierda"

            self._dynamicButtonsBinds[fieldName] = self._menu.add.button(f"Mover {movimiento}: '{keyName}'",
                                                                         self._editBinding, fieldName,
                                                                         font_color=backgroundColorText,
                                                                         font_shadow=True, font_shadow_offset=1,
                                                                         font_shadow_color=font_shad_color,
                                                                         selection_color=sel_color)
            self._dynamicButtonsTitle[fieldName] = f"Mover {movimiento}: "

    def _editVolume(self, value, field):
        """
        Updates the configuration value of the volume field given
        """
        value = round(float(value) / 100, 2)
        ConfManager.setValue(field, value)

        if field == "sound.menu_music_volume":
            pygame.mixer.music.set_volume(value)

    def _loadVolumeSettings(self):
        """
        Loads the volume settings and creates a button to edit each of them
        """

        menuVolume = int(float(ConfManager.getValue("sound.menu_music_volume") * 100))
        self._menu.add.range_slider('Menu', menuVolume, (0, 100), 1,
                                    value_format=lambda x: str(int(x)),
                                    onchange=self._editVolume, field="sound.menu_music_volume",
                                    font_color=backgroundColorText,
                                    font_shadow=True, font_shadow_offset=1, font_shadow_color=font_shad_color,
                                    selection_color=sel_color)

        gameVolume = int(float(ConfManager.getValue("sound.game_music_volume") * 100))
        self._menu.add.range_slider('Juego', gameVolume, (0, 100), 1,
                                    value_format=lambda x: str(int(x)),
                                    onchange=self._editVolume, field="sound.game_music_volume",
                                    font_color=backgroundColorText,
                                    font_shadow=True, font_shadow_offset=1, font_shadow_color=font_shad_color,
                                    selection_color=sel_color)

        soundEffectsVolume = int(float(ConfManager.getValue("sound.sound_effects_volume") * 100))
        self._menu.add.range_slider('Sonidos', soundEffectsVolume, (0, 100), 1,
                                    value_format=lambda x: str(int(x)),
                                    onchange=self._editVolume, field="sound.sound_effects_volume",
                                    font_color=backgroundColorText,
                                    font_shadow=True, font_shadow_offset=1, font_shadow_color=font_shad_color,
                                    selection_color=sel_color)