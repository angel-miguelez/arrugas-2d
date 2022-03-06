# -*- coding: utf-8 -*-

import pygame


def _collideCollisionRect(left, right):
    return left.collisionRect.colliderect(right.rect)


class Interactive:
    """
    Base class to implement a simple collision system based on sprite.rect
    """

    def __init__(self, rect):

        self.collisionRect = rect  # rect used to detect the collisions

        self.objectsEnterCollision = []  # objects that have just collide
        self.objectsExitCollision = []  # objects that have stopped colliding
        self.objectsStayCollision = []  # objects that have been colliding for more than one frame
        self.collisionGroups = []  # groups to which detect collisions

    def _detectCollision(self):
        """
        Method that checks the collision between the object and the collision groups. It updates
        the state of each object/collision (enter, stay, exit)
        """

        colliding = []  # list of objects which are colliding right now

        self.objectsExitCollision.clear()  # an object can exit a collision only once

        # Register all the objects that are colliding, and we are interested in
        for group in self.collisionGroups:
            colliding = colliding + pygame.sprite.spritecollide(self, group, dokill=False, collided=_collideCollisionRect)

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

    def updateCollisions(self, *args):
        self._detectCollision()

    def addCollisionGroup(self, group):
        """
        Adds a new group to check collisions with
        """

        if group not in self.collisionGroups:
            self.collisionGroups.append(group)

    def changeCollisionRect(self, rect):
        """
        Changes the Rect used to check the collisions
        """

        self.collisionRect = rect
