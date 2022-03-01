# -*- coding: utf-8 -*-
import pygame.key

from utils.resourcesmanager import *
import itertools
from utils.observer import Subject
import math

# Movement direction constants
LEFT, RIGHT, UP, DOWN = 0, 1, 2, 3
IDLE = 4
UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT = 5, 6, 7, 8

DIAG_FACTOR = math.sqrt(2) / 2  # avoid diagonal movements been faster than the others


class Character(pygame.sprite.Sprite):
    """
    Class that represents every character in the game
    """

    def __init__(self, imageFile, coordFile, sheetDimension, coordScreen, scale, speed, animationDelay, updateByTime, walls=None):
        """
        imageFile -> file with image data
        coordFile -> File with all the coordinades of the sprites from imageFile
        sheetDimension -> array with the number of diferent sprites. ex: [4, 4] 2 positions with 4 different sprites each position
        coordScreen -> coordinates on screen where sprite is initialized
        scale -> size of the sprites
        speed -> speed of the player
        animationDelay -> delay on each movement of the characters
        updateByTime -> if sprite is updated every moment(basic0) or updated while moving(player)
        walls -> group of sprites that the player can not step over
        """

        pygame.sprite.Sprite.__init__(self)

        # Load and split the sprite sheet
        self.sheet = ResourcesManager.loadImage(imageFile, -1)
        data = ResourcesManager.loadCoordFile(coordFile)
        data = list(map(lambda x: int(x), data.split()))
        self.sheetCoord = self._processSpriteSheet(data, sheetDimension)

        # Sprite posture
        self.posture = DOWN
        self.subPosture = 0  # column position in the posture (row)
        self.animationDelay = animationDelay  # time to wait to update the next image
        self.timeToUpdateSprite = 0

        self.updateByTime = updateByTime

        # Initialize sprite image and rect
        self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][self.subPosture]), scale)
        self.rect = self.image.get_rect()
        self.scale = scale  # size of the image

        # Initial position on the screen
        self.x, self.y = (coordScreen[0], coordScreen[1])
        self.lastPos = (self.x, self.y)  # used to revert the last movement if it collided with a wall
        self.rect.left = self.x
        self.rect.bottom = self.y

        # Movement related variables
        self.movement = IDLE
        self.xShift, self.yShift = (0, 0)
        self.speed = speed
        self.walls = walls  # to check movement collisions

    def _processSpriteSheet(self, sheet, sheetDimension):
        """
        Iterates over the sheet saving the different sprites into a list
        """

        out = []
        cont = 0

        for line in range(0, len(sheetDimension)):
            out.append([])  # create a new posture
            tmp = out[line]

            for position in range(1, sheetDimension[line] + 1):  # iterate over the subpostures
                tmp.append(Rect((sheet[cont], sheet[cont + 1]), (sheet[cont + 2], sheet[cont + 3])))
                cont += 4

        return out

    def updateImage(self):
        """
        Updates the current image of the sprite, if the counter has reached 0
        """

        self.timeToUpdateSprite -= 1
        if self.timeToUpdateSprite > 0:  # we have to wait more time to update the image
            return

        self.timeToUpdateSprite = self.animationDelay  # reset the counter
        self.subPosture += 1  # go to the next subposture in the row

        # If we have reached the last subposture, return to the initial one
        if self.subPosture >= len(self.sheetCoord[self.posture]):
            self.subPosture = 0

        # Update the image
        image = self.sheet.subsurface(self.sheetCoord[self.posture][self.subPosture])
        self.image = pygame.transform.scale(image, self.scale)

        # no movement is being done
        if self.updateByTime == 0 and self.movement == IDLE:
            self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][0]), self.scale)

    def update(self, time):

        # Reset previous movement shift
        self.xShift = 0
        self.yShift = 0

        # Calculate the shift in x and y direction and set the corresponding posture depending on the movement
        shift = int(self.speed * time)
        if self.movement == LEFT:
            self.posture = LEFT
            self.xShift = - shift
        elif self.movement == RIGHT:
            self.posture = RIGHT
            self.xShift = shift
        elif self.movement == UP:
            self.posture = UP
            self.yShift = - shift
        elif self.movement == DOWN:
            self.posture = DOWN
            self.yShift = shift
        # elif self.movement == UP_LEFT:
        #     self.posture = UP
        #     self.yShift = - int(DIAG_FACTOR * self.speed * time)
        #     self.xShift = -int(DIAG_FACTOR * self.speed * time)
        # elif self.movement == UP_RIGHT:
        #     self.posture = UP
        #     self.yShift = - int(DIAG_FACTOR * self.speed * time)
        #     self.xShift = int(DIAG_FACTOR * self.speed * time)
        # elif self.movement == DOWN_LEFT:
        #     self.posture = DOWN
        #     self.yShift = int(DIAG_FACTOR * self.speed * time)
        #     self.xShift = - int(DIAG_FACTOR * self.speed * time)
        # elif self.movement == DOWN_RIGHT and self.lastMovement == DOWN:
        #     self.posture = RIGHT
        #     self.movement = RIGHT
        #     self.xShift = shift
        # elif self.movement == DOWN_RIGHT and self.lastMovement == RIGHT:
        #     self.posture = DOWN
        #     self.movement = DOWN
        #     self.yShift = shift
        elif self.movement == IDLE:  # no movement updates in IDLE state
            pass

        self.updateImage()
        self.lastPos = (self.x, self.y)
        self.x += self.xShift
        self.y += self.yShift

    def pillEffect(self):
        self.speed = self.speed * 0.5
        

def _collideCollisionRect(left, right):
    return left.legsRect.colliderect(right.rect)


class Player(Character, Subject):
    """
    Class that represents the playable character
    """""

    def __init__(self, pos, walls):
        Subject.__init__(self)
        Character.__init__(self, 'character.png', 'coordMan.txt', [3, 3, 3, 3], pos, (30, 30), 0.1, 4, 0, walls)

        # We use a new rect that is placed at the bottom body-upper legs of the sprite to detect collisions
        self.legsRect = self.rect.copy()
        self.legsRect.inflate_ip(-5, -13)
        self.legsRect.bottom = self.rect.bottom - 2
        self.legsRect.left = self.rect.left + (self.rect.width - self.legsRect.width) / 2

        # Load the movement bindings from the configuration file
        self.MOVE_UP, self.MOVE_DOWN, self.MOVE_RIGHT, self.MOVE_LEFT = ConfManager().getPlayerMovementBinds()
        self.lastMovements = [IDLE]  # ordered sequence of movement keys pressed by the user (more info in move method)

        self.eventsEnabled = True

        self.hasPills = 0

    def increaseSpeed(self):
        self.speed *= 1.5

    def disableEvents(self):
        self.eventsEnabled = False

    def enableEvents(self):
        self.eventsEnabled = True

    def move(self, toggledKeys):
        """
        Updates the movement state, depending on the keys being pressed
        """

        if toggledKeys[self.MOVE_UP] and toggledKeys[self.MOVE_LEFT]:
            self.movement = UP_LEFT
        elif toggledKeys[self.MOVE_UP] and toggledKeys[self.MOVE_RIGHT]:
            self.movement = UP_RIGHT
        elif toggledKeys[self.MOVE_DOWN] and toggledKeys[self.MOVE_LEFT]:
            self.movement = DOWN_LEFT
        elif toggledKeys[self.MOVE_DOWN] and toggledKeys[self.MOVE_RIGHT]:
            self.movement = DOWN_RIGHT
        elif toggledKeys[self.MOVE_UP]:
            self.movement = UP
        elif toggledKeys[self.MOVE_LEFT]:
            self.movement = LEFT
        elif toggledKeys[self.MOVE_RIGHT]:
            self.movement = RIGHT
        elif toggledKeys[self.MOVE_DOWN]:
            self.movement = DOWN
        else:
            self.movement = IDLE

    def move(self, event):
        """
        The player can press multiple keys in a row, but the current movement will correspond only to the last key
        pressed. We save the order in which these keys were pressed, so if the last one (current movement) is released
        we recover the previous movement.

        For example, if the player is going to the left and presses the MOVE_RIGHT button (without releasing MOVE_LEFT),
        the movement will be to the right. Now, if it releases MOVE_RIGHT, the movement will back to be to the left.
        This way, when a key is pressed we append it to the list, and if is released the key is removed from it.
        """

        # Update the current movement to the current key pressed
        if event.type == KEYDOWN:

            if event.key == self.MOVE_LEFT:
                self.movement = LEFT
                self.lastMovements.append(LEFT)
            elif event.key == self.MOVE_RIGHT:
                self.movement = RIGHT
                self.lastMovements.append(RIGHT)
            elif event.key == self.MOVE_UP:
                self.movement = UP
                self.lastMovements.append(UP)
            elif event.key == self.MOVE_DOWN:
                self.movement = DOWN
                self.lastMovements.append(DOWN)

        # Remove from the list the key
        elif event.type == KEYUP:

            if event.key == self.MOVE_LEFT:
                self.lastMovements.remove(LEFT)
            elif event.key == self.MOVE_RIGHT:
                self.movement = RIGHT
                self.lastMovements.remove(RIGHT)
            elif event.key == self.MOVE_UP:
                self.movement = UP
                self.lastMovements.remove(UP)
            elif event.key == self.MOVE_DOWN:
                self.movement = DOWN
                self.lastMovements.remove(DOWN)

    def events(self, events):

        if not self.eventsEnabled:
            self.movement = IDLE
            return

        # self.move(pygame.key.get_pressed())  # update the movement state
        for event in events:
            self.move(event)


    def update(self, time):

        self.movement = self.lastMovements[-1]  # the last key pressed by the user

        # Update the position and notify observers (walls)
        super().update(time)
        self.notify()

        # Check if there was a collision
        collidedHor, collidedVer = (False, False)
        collided = pygame.sprite.spritecollide(self, self.walls, False, _collideCollisionRect)

        if len(collided) > 0:

            for sprite in collided:

                # Distinguish between a horizontal and vertical collision, based on the relative position of the centers
                # and the maximum distance it can be between them in the vertical and horizontal collision respectively

                difference = abs(self.legsRect.center[1] - sprite.rect.center[1])  # distance between centers.y
                maxDifference = self.legsRect.height / 2 + sprite.rect.height / 2

                # If the difference is almost the maximum difference in vertical, then they collided vertically
                if maxDifference - difference < 10:
                    collidedVer = True

                difference = abs(self.legsRect.center[0] - sprite.rect.center[0])  # distance between centers.x
                maxDifference = self.legsRect.width / 2 + sprite.rect.width / 2

                # If the difference is almost the maximum difference in horizontal, then they collided horizontally
                if maxDifference - difference < 10:
                    collidedHor = True

        if collidedHor:
            self.x = self.lastPos[0]  # undo the horizontal movement
        if collidedVer:
            self.y = self.lastPos[1]  # undo the vertical movement

        self.lastPos = (self.x, self.y)
        self.notify()  # notify again to draw the level properly

    def getPos(self):
        return self.x, self.y

    def getPill(self):
        self.hasPills=self.hasPills+1

    def usePill(self, grupo):
        #if self.hasPills==0:
            #Sonido incorrecto
        #else:
        if self.hasPills>0:
            self.hasPills=self.hasPills-1
            grupo.pillEffect()


class Enemy(Character):

    def update(self, time):
        super().update(time)
        self.rect.bottom = self.y
        self.rect.left = self.x

class WalkingEnemy(Enemy):
    def __init__(self, imageFile, coordFile, sheetDimension, coordScreen, scale, speed, animationDelay, updateByTime, waypoints):
        Character.__init__(self, imageFile, coordFile, sheetDimension, coordScreen, scale, speed, animationDelay, updateByTime);
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2((self.x, self.y))
        self.target_radius = 20
        self.waypoints = itertools.cycle(waypoints)
        self.target = next(self.waypoints)
        self.orientationvector=itertools.cycle((RIGHT, LEFT))
        self.orientation=next(self.orientationvector)

    def update(self, time):
        # A vector pointing from self to the target.
        heading = self.target - self.pos
        if(heading[0] > 0):
            self.movement = LEFT
            self.looking = LEFT
            self.positionNum = 0
        else:
            self.movement = RIGHT
            self.movement = RIGHT
            self.positionNum = 1
        distance = heading.length()  # Distance to the target.
        heading.normalize_ip()
        if distance <= 2:  # We're closer than 2 pixels.
            # Increment the waypoint index to swtich the target.
            # The modulo sets the index back to 0 if it's equal to the length.
            self.target = next(self.waypoints)
            self.orientation = next(self.orientationvector)
        if distance <= self.target_radius:
            # If we're approaching the target, we slow down.
            self.vel = heading * (distance / self.target_radius * self.speed)
        else:  # Otherwise move with max_speed.
            self.vel = heading * self.speed

        self.pos += self.vel
        self.rect.center = self.pos
        super().updateImage()
       

# -------------------------------------------------
# Basic enemy 0 class

class Basic0(Enemy):
    def __init__(self,coordScreen):
        # called constructor of father class
        Character.__init__(self, 'B0.png', 'coordBasic0.txt', [7], coordScreen, (32,32), 0.3, 5, 0.5);


# -------------------------------------------------
# Basic enemy 1 class

class Basic1(WalkingEnemy):
    def __init__(self, coordScreen, waypoints, speed):
        # called constructor of father class
        WalkingEnemy.__init__(self, 'B1.1.png', 'coordBasic1.1.txt', [6,6], coordScreen, (32,32), speed, 5, 0.5, waypoints);


# -------------------------------------------------
# Basic enemy 1 class

class Basic2(Enemy):
    def __init__(self, coordScreen, player):
        # called constructor of father class
        self.radius=200
        self.enemy=player
        Character.__init__(self, 'B2.png', 'coordBasic2.txt', [10], coordScreen, (148,120), 0.3, 5, 0.5);
        

    def updateImage(self):
        self.timeToUpdateSprite -= 1
        # check if time between sprites updates

        self.pos = pygame.math.Vector2((self.x, self.y))
        self.target = (self.enemy.x, self.enemy.y)
        heading = self.target - self.pos
        distance = heading.length() 
        heading.normalize_ip()
        if distance <= self.radius:   
            if (self.timeToUpdateSprite < 0):
                self.movementDelay = self.animationDelay
                # update sprite
                self.subPosture += 1
                if self.subPosture >= len(self.sheetCoord[self.posture]):
                    self.imagePositionNum = 0;
                if self.imagePositionNum < 0:
                    self.imagePositionNum = len(self.sheetCoord[self.posture]) - 1
                self.image= pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][self.imagePositionNum]), self.scale)
        else:
            # no movement is being done
            if self.movement == IDLE:
                self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][0]), self.scale)
            

# -------------------------------------------------
# Normal enemy 2 

class Normal2(Enemy):
    "Normal2 enemy 3"
    def __init__(self, coordScreen):
        # called constructor of father class
        Character.__init__(self, 'N2.2.png', 'coordNormal2.2.txt', [3,3,3,3],coordScreen, (32,50), 0.1, 5, 0);

        #move function that chase the player
    def move(self, player, area):
        # tracked player
        # area where the player is going to be tracked
        if (abs(self.x - player.x) < area) and (abs(self.y - player.y) < area):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
            if ((self.x - player.x) == 0) and ((self.y - player.y) == 0):
                 self.movement = IDLE
            elif ((self.x - player.x) == 0) and ((self.y - player.y) > 0):
                 self.movement = UP
            elif ((self.x - player.x) == 0) and ((self.y - player.y) < 0):
                 self.movement = DOWN
            elif ((self.x - player.x) < 0) and ((self.y - player.y) == 0):
                 self.movement = RIGHT
            elif ((self.x - player.x) > 0) and ((self.y - player.y) == 0):
                 self.movement = LEFT
            elif ((self.x - player.x) < 0) and ((self.y - player.y) < 0):
                 self.movement = DOWN
            elif ((self.x - player.x) > 0) and ((self.y - player.y) > 0):
                 self.movement = UP
            elif ((self.x - player.x) < 0) and ((self.y - player.y) > 0):
                 self.movement = RIGHT
            elif ((self.x - player.x) > 0) and ((self.y - player.y) < 0):
                 self.movement = LEFT
        else:
             self.movement = IDLE



# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def main():

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((800, 600), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Poner el título de la ventana
    pygame.display.set_caption('Ejemplo de uso de Sprites')

    # Creamos los jugadores
    #jugador1 = Character('old_man.png', 'coordMan.txt', [3,3,3,3],[300, 100], 0.3, 0)
    jugador1 = Player()
    basic0 = Basic0([100, 100])
    
    waypoints=[(360,200),(140,200)]
    spawn=[140, 200]

    basic1=Basic1(spawn, waypoints, 1.5)

    basic2 = Basic2([500, 500], jugador1)
    
    normal2 = Normal2([500, 100])
    
    # Creamos el grupo de Sprites de jugadores
    grupoJugadores = pygame.sprite.Group( jugador1, basic0, basic1, basic2, normal2 )


    # El bucle de eventos
    while True:

        # Hacemos que el reloj espere a un determinado fps
        time_pasado = reloj.tick(60)

        # Para cada evento, hacemos
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Miramos que teclas se han pulsado
        toggledKeys = pygame.key.get_pressed()

        # Si la tecla es Escape
        if toggledKeys[K_ESCAPE]:
            # Se sale del programa
            pygame.quit()
            sys.exit()

        # Si la tecla es X
        if toggledKeys[K_x]:
            # Se ejecuta mecánica pastillas
            jugador1.hasPills()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        jugador1.move(toggledKeys, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        normal2.move(jugador1, 200)

        # Actualizamos los jugadores actualizando el grupo
        grupoJugadores.update(time_pasado)


        # Dibujar el fondo de color
        pantalla.fill((133,133,133))

        # Dibujar el grupo de Sprites
        grupoJugadores.draw(pantalla)
        
        # Actualizar la pantalla
        pygame.display.update()


if __name__ == "__main__":
    main()
