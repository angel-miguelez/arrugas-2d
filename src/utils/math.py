# -*- coding: utf-8 -*-

import pygame
from pygame.math import Vector2

def getCollisionPoint(sprite1, sprite2):
    origin = Vector2(sprite1.rect.center)
    target = Vector2(sprite2.rect.center)

    dir = target - origin
    length = dir.length()
    dir = dir.normalize()

    currentPos = origin
    for _ in range(0, int(length)):
        currentPos += dir
        if sprite2.rect.collidepoint(currentPos):
            return currentPos

def getCollisionPoint2(origin, dir, target):
    rect = target
    origin = Vector2(origin.center)
    target = Vector2(target.center)
    length = (origin-target).length()
    dir = Vector2(dir)

    currentPos = origin
    for _ in range(0, int(length)):
        currentPos += dir
        if rect.collidepoint(currentPos):
            return currentPos




