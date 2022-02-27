# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from conf.configuration import ConfManager
from game.director import Director
from utils.observer import Observer, Subject
from utils.resourcesmanager import ResourcesManager


class Dialogue(Observer):

    def __init__(self):
        self.interventions = []
        self.currentIntervention = 0
        self.active = False

    # def update(self, subject: Subject) -> None:
    #     self.next()

    def add(self, intervention):
        self.interventions.append(intervention)
        intervention.attach(self)

    def next(self):

        self.currentIntervention += 1
        if self.currentIntervention == len(self.interventions):
            Director().getCurrentScene().player.enableEvents()
            self.active = False
        else:
            self.interventions[self.currentIntervention].start()

    def clear(self):
        self.interventions.clear()
        self.currentIntervention = 0

    def start(self):
        self.active = True
        self.currentIntervention = 0
        Director().getCurrentScene().player.disableEvents()
        self.interventions[0].start()

    def events(self, events):

        if not self.active:
            return

        self.interventions[self.currentIntervention].events(events)

    def update(self, *args):

        if isinstance(args[0], DialogueIntervention):
            self.next()
            return

        if not self.active:
            return

        self.interventions[self.currentIntervention].update(*args)

    def draw(self, surface):

        if not self.active:
            return

        self.interventions[self.currentIntervention].draw(surface)


class TextUI:
    """
    Class to draw some text in the screen
    """

    def __init__(self, font, size, position=(0, 0), color=(0, 0, 0), antialiasing=True):

        # Font properties
        self.font = ResourcesManager.loadFont(font, size)
        self.color = color
        self.antialiasing = antialiasing
        self.text = None

        self.position = position  # position in the world

        self.active = False  # only rendered while active

    def setText(self, text):
        """
        Updates the text
        """
        self.text = self.font.render(text, self.antialiasing, self.color)

    def draw(self, surface):
        if self.active:
            surface.blit(self.text, self.position)

    def activate(self):
        """
        Sets the text to activated, so it is rendered on the screen
        """
        self.active = True

    def deactivate(self):
        """
        Sets the object to desactivated, so it is not rendered on the screen
        """
        self.active = False


class DialogueIntervention(TextUI, Subject):
    """
    Class to draw some text on a dialogue box, with an avatar of the character who is speaking
    """

    def __init__(self):
        Subject.__init__(self)

        self.done = False

        font = ConfManager.getValue("dialogue.font")
        size = int(ConfManager.getValue("dialogue.font_size"))
        color = eval(ConfManager.getValue("dialogue.color"))
        antialiasing = ConfManager.getValue("dialogue.antialiasing") == "True"
        super().__init__(font, size, color=color, antialiasing=antialiasing)

        self.avatar = None
        self.avatarPosition = (110, 480)

        self.box = ResourcesManager.loadImage("paper-dialog.png", transparency=True)
        self.boxPosition = (140, 500)

        self.lines = []  # lines are elements of the text separated by '\n'
        self.linesPosition = (212, 510)  # where the first char is drawn
        self.linesSpacing = size * 0.8  # space between lines

    def start(self):
        pass

    def events(self, events):

        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE and self.done:
                self.notify()

    def update(self, *args):
        self.done = True

    def draw(self, surface):

        surface.blit(self.box, self.boxPosition)
        surface.blit(self.avatar, self.avatarPosition)

        for idx, line in enumerate(self.lines):
            surface.blit(line, (self.linesPosition[0], self.linesPosition[1] + idx * self.linesSpacing))

    def clear(self):
        """
        Clear the list of lines
        """
        self.lines.clear()

    def setLine(self, text, idx):
        """
        Updates the text of the line at index 'idx' in the text
        """
        render = self.font.render(text, self.antialiasing, self.color)  # creates the pygame surface
        try:
            self.lines[idx] = render
        except IndexError:  # no line was added before at that position
            self.lines.append(render)

    def setText(self, text):
        """
        Updates the text of the dialogue
        """
        for idx, line in enumerate(text):
            self.setLine(line, idx)

    def setAvatar(self, avatar):
        self.avatar = ResourcesManager.loadImage(avatar, transparency=True)


class DynamicDialogueIntervention(DialogueIntervention):
    """
    Dialogue whose text is rendered progessively
    """

    def __init__(self):
        super().__init__()

        self._gen = None  # generator that returns the line updated with the new char
        self.text = ""  # all the paragraphs of the dialogue, each paragraph is rendered separated
        self.done = True  # True if the last paragraph has been rendered

        self.currentParagraphText = ""  # the current paragraph being rendered
        self.currentParagraph = 0  # position of the current paragraph in the text
        self.paragraphDone = True  # True if the paragraph has been rendered completly

        self.currentLine = 0  # current line of the paragraph being rendered

        self.nextCharTime = ConfManager.getValue("dialogue.delay_between_chars")  # ms to wait to render the next char
        self.timeSinceLastChar = 0  # ms passed since the last char rendered

    def start(self):
        """
        Sets the object activated, and load the first line of the first paragraph into the generator
        """
        super().activate()

        self.reset()

        self.currentParagraphText = self.text[0]
        self._gen = self._textGenerator(self.currentParagraphText[0])  # pass the first line of the first paragraph to the generator

    def events(self, events):

        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:

                if self.done:
                    self.notify()

                elif self.paragraphDone:
                    self.nextParagraph()

                else:
                    self.completeParagraph()

    def update(self, time):

        if self.done or self.paragraphDone:
            return

        try:
            # Update the time since the last char generated and check if it is time to generate one more
            self.timeSinceLastChar += time
            if self.timeSinceLastChar < self.nextCharTime:
                return

            self.timeSinceLastChar = 0  # reset the counter
            self._generateNextChar()

        except StopIteration:  # line finished

            if self.currentLine == len(self.currentParagraphText) - 1:  # all the lines rendered
                self.paragraphDone = True

                if self.currentParagraph == len(self.text) - 1:  # all the paragraphs rendered
                    self.done = True

            else:
                self._createGeneratorNextLine()  # add the next line to the generator

    def setText(self, text):
        self.text = text

    # Based on https://stackoverflow.com/questions/31381169/pygame-scrolling-dialogue-text
    # It returns the next character of the phrase in every call
    def _textGenerator(self, phrase):
        tmp = ''
        for letter in phrase:
            tmp += letter
            # don't pause for spaces
            if letter != ' ':
                yield tmp

    def _generateNextChar(self, complete=False):
        """
        Adds the next char of the line. If 'complete', the whole line is added to render
        """

        text = self.currentParagraphText[self.currentLine] if complete else next(self._gen)
        self.setLine(text, self.currentLine)

    def _createGeneratorNextLine(self):
        """
        Sets the next line to the generator
        """

        self.currentLine += 1
        self._gen = self._textGenerator(self.currentParagraphText[self.currentLine])

    def clear(self):
        """
        Removes the content of the current lines being rendered
        """

        super().clear()
        self.currentLine = 0

    def reset(self):
        """
        Sets all the variables to their initial state
        """

        self.clear()

        self.currentParagraph = 0
        self.paragraphDone = False
        self.done = False

    def nextParagraph(self):
        """
        Adds the next paragraph to the generator, removing the current one
        """

        self.clear()

        self.currentParagraph += 1
        self.currentParagraphText = self.text[self.currentParagraph]
        self._gen = self._textGenerator(self.currentParagraphText[0])  # add the first line of the paragraph
        self.paragraphDone = False

    def completeParagraph(self):
        """
        Completes the content of the current paragraph, so the delay is not waited
        """

        # Complete every line of the paragraph
        for i in range(self.currentLine, len(self.currentParagraphText)):
            self.currentLine = i
            self._generateNextChar(complete=True)

        # Check if all the text has been rendered
        self.paragraphDone = True
        if self.currentParagraph == len(self.text) - 1:
            self.done = True
