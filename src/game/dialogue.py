# -*- coding: utf-8 -*-
import os

from pygame.locals import *

from conf.configuration import ConfManager
from game.director import Director
from utils.observer import Observer, Subject
from utils.resourcesmanager import ResourcesManager


class Dialogue(Observer):

    def __init__(self):
        self.interventions = []  # list of all the interventions in the dialogue
        self.currentIntervention = 0  # the current intervention being played

        self.scene = None
        self.finished = False

    def updateObserver(self, subject):
        self.next()

    def add(self, intervention):
        """
        Adds a new interventions to the tail of the interventions. If a dialogue was played before,
        we must call clear() before adding the new interventions to clean the state.
        """

        self.interventions.append(intervention)
        intervention.attach(self)  # so we know when the intervention has finished (it notifies)

    def next(self):
        """
        Plays the next intervention in the list, if there is any, otherwise the dialogue is closed
        """

        self.currentIntervention += 1
        if self.currentIntervention == len(self.interventions):  # the dialogue has finished, closed it
            self.scene.removeFromGroup(self, "uiGroup")
            self.scene.removeFromGroup(self, "objectsToEvent")
            self.scene.removeFromGroup(self, "objectsToUpdate")
            self.scene.unpauseEvents()
            self.finished = True
        else:
            self.interventions[self.currentIntervention].start()  # start the next intervention

    def clear(self):
        """
        Sets the state of the dialogue to the initial state (no interventions)
        """

        self.interventions.clear()
        self.currentIntervention = 0

    def start(self):
        """
        Starts the dialogue, playing the first intervention.
        """

        self.finished = False

        self.scene = Director().getCurrentScene()  # the scene where the dialogue is going to be played
        self.scene.pauseEvents()  # the dialogue will be the only object receiving events

        self.scene.addToGroup(self, "uiGroup")
        self.scene.addToGroup(self, "objectsToEvent")
        self.scene.addToGroup(self, "objectsToUpdate")

        self.interventions[0].start()  # start the first intervention

    def events(self, events):
        self.interventions[self.currentIntervention].events(events)

    def update(self, *args):
        self.interventions[self.currentIntervention].update(*args)

    def draw(self, surface):
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
        surface.blit(self.text, self.position)


class SimpleDialogueIntervention(TextUI, Subject):
    """
    Class to draw some text on a dialogue box, with an avatar of the character who is speaking
    """

    def __init__(self):
        Subject.__init__(self)

        # Font properties
        font = ConfManager.getValue("dialogue.font")
        size = int(ConfManager.getValue("dialogue.font_size"))
        color = eval(ConfManager.getValue("dialogue.color"))
        antialiasing = ConfManager.getValue("dialogue.antialiasing") == "True"
        super().__init__(font, size, color=color, antialiasing=antialiasing)

        # Avatar
        self.avatar = None
        self.avatarPosition = (110, 483)

        # Dialogue box
        self.box = ResourcesManager.loadImage("paper-dialog.png", transparency=True)
        self.boxPosition = (140, 500)

        # The text whole text
        self.done = False
        self.text = None  # the whole text, a list of paragraphs
        self.currentParagraph = 0  # position of the current paragraph in the text
        self.lines = []  # lines are elements of the paragraph separated by '\n'
        self.linesPosition = (212, 510)  # where the first char is drawn
        self.linesSpacing = size * 0.8  # space between lines

    def start(self):
        self.currentParagraph = -1
        self.nextParagraph()

    def events(self, events):

        for event in events:

            if event.type == KEYDOWN and event.key == K_SPACE:

                if self.done:
                    self.notify()  # notify when all the text has been rendered
                else:
                    self.nextParagraph()  # render the next paragraph

    def update(self, *args):
        pass

    def draw(self, surface):
        surface.blit(self.box, self.boxPosition)
        surface.blit(self.avatar, self.avatarPosition)

        for idx, line in enumerate(self.lines):  # iterate over the lines, rendering each of them
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
        self.text = text

    def setAvatar(self, avatar):
        self.avatar = ResourcesManager.loadImage(os.path.join("avatar", avatar), transparency=True)

    def nextParagraph(self):
        """
        Sets the text of the next paragraph
        """

        self.clear()  # clear the previous lines

        self.currentParagraph += 1

        for idx, line in enumerate(self.text[self.currentParagraph]):  # render the next paragraph
            self.setLine(line, idx)

        if self.currentParagraph == len(self.text) - 1:  # all the paragraphs has been rendered
            self.done = True


class DynamicDialogueIntervention(SimpleDialogueIntervention):
    """
    Dialogue whose text is rendered progessively
    """

    def __init__(self):
        super().__init__()

        self._gen = None  # generator that returns the line updated with the new char
        self.currentParagraphText = ""  # list of lines of the current paragraph
        self.paragraphDone = False

        self.currentLine = 0  # current line of the paragraph being rendered

        self.nextCharTime = ConfManager.getValue("dialogue.delay_between_chars")  # ms to wait to render the next char
        self.timeSinceLastChar = 0  # ms passed since the last char rendered

    def events(self, events):

        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:

                if self.done:  # all paragraphs rendered
                    self.notify()

                elif self.paragraphDone:  # the current paragraph rendered completely
                    self.nextParagraph()

                else:
                    self.completeParagraph()  # complete the paragraph without delay

    def update(self, time):

        if self.paragraphDone:
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

    def clear(self):
        super().clear()
        self.currentLine = 0

    def nextParagraph(self):
        self.clear()  # clear the previous lines

        self.currentParagraph += 1
        self.currentParagraphText = self.text[self.currentParagraph]
        self._gen = self._textGenerator(self.currentParagraphText[0])  # add the first line of the paragraph
        self.paragraphDone = False

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
