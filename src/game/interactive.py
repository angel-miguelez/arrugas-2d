# -*- coding: utf-8 -*-

import pygame

from utils.resourcesmanager import ResourcesManager


class Interactive(pygame.sprite.Sprite):
    """
    Base class to implement a simple collision system based on sprite.rect
    """

    def __init__(self, image, collisionGroups, position=(0, 0), name=None):
        pygame.sprite.Sprite.__init__(self)

        # Load image and rect to detect collisions
        self._initializeSprite(image, position)

        self.objectsEnterCollision = []  # objects that have just collide
        self.objectsExitCollision = []  # objects that have stopped colliding
        self.objectsStayCollision = []  # objects that have been colliding for more than one frame
        self.collisionGroups = collisionGroups  # groups to which detect collisions

        self.name = self.__class__.__name__ if name is None else name  # identifier for the object in collisions

    def update(self, time):
        self._detectCollision()

    def _initializeSprite(self, image, position):
        """
        Creates the image and the rect of the sprite, placing it in a specific position
        """

        self.image = ResourcesManager.loadImage(image, transparency=True)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def _detectCollision(self):
        """
        Method that checks the collision between the object and the collision groups. It updates
        the state of each object/collision (enter, stay, exit)
        """

        colliding = []  # list of objects which are colliding right now

        self.objectsExitCollision.clear()  # an object can exit a collision only once

        # Register all the objects that are colliding, and we are interested in
        for group in self.collisionGroups:
            colliding = colliding + pygame.sprite.spritecollide(self, group, dokill=False)

        # If an object is no longer colliding, it has exited the collision
        for collided in (self.objectsEnterCollision + self.objectsStayCollision):
            if collided not in colliding:

                # Remove the object from the list in which it was registered
                try:
                    self.objectsEnterCollision.remove(collided)
                except ValueError:
                    pass

                try:
                    self.objectsStayCollision.remove(collided)
                except ValueError:
                    pass

                # Register the object as an object that has exited the collision
                self.objectsExitCollision.append(collided)
                self.onCollisionExit(collided)

        # Check the states of each collision
        for collided in colliding:

            # If it was entered before, now it stays in collision
            if collided in self.objectsEnterCollision:
                self.objectsEnterCollision.remove(collided)
                self.objectsStayCollision.append(collided)
                self.onCollisionStay(collided)

            # If it was staying the collision, remains the same
            elif collided in self.objectsStayCollision:
                self.onCollisionStay(collided)

            # If is a new collision, it entered in collision
            else:
                self.objectsEnterCollision.append(collided)
                self.onCollisionEnter(collided)

    # Override these methods to get the expected behaviour on each subclass.
    # Typically, you will check the collision.object or collision.name
    # to decide what action should be done depending on the object
    # that has been collided.
    def onCollisionEnter(self, collided):
        pass

    def onCollisionExit(self, collided):
        pass

    def onCollisionStay(self, collided):
        pass