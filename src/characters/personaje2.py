# -*- coding: utf-8 -*-
from pickle import TRUE
import pygame.key
from characters.entity import Entity

from characters.entity import Entity
from game.interactive import Interactive
from game.director import Director
from map.tiles import Tile
from utils.resourcesmanager import *
import itertools
from utils.observer import Subject
import math

# Movement direction constants
LEFT, RIGHT, UP, DOWN = 0, 1, 2, 3
IDLE = 4
UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT = 5, 6, 7, 8

DIAG_FACTOR = math.sqrt(2) / 2  # avoid diagonal movements been faster than the others


class Character(pygame.sprite.Sprite, Interactive):
    """
    Class that represents every character in the game
    """

    def __init__(self, imageFile, coordFile, sheetDimension, position, scale, speed, animationDelay, updateByTime):
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
        self.posture = LEFT
        self.subPosture = 0  # column position in the posture (row)
        self.animationDelay = animationDelay  # time to wait to update the next image
        self.timeToUpdateSprite = 0  # counter

        self.updateByTime = updateByTime

        # Initialize sprite image and rect
        self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][self.subPosture]), scale)
        self.rect = self.image.get_rect()
        self.scale = scale  # size of the image

        # Initialize collision system to collide with the walls
        Interactive.__init__(self, self.rect)

        # Initial position on the screen
        self.x, self.y = (position[0], position[1])
        self.lastPos = (self.x, self.y)  # used to revert the last movement if it collided with a wall
        self.rect.left = self.x
        self.rect.bottom = self.y

        # Movement related variables
        self.movement = IDLE
        self.xShift, self.yShift = (0, 0)
        self.speed = speed

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
        elif self.movement == IDLE:  # no movement updates in IDLE state
            pass

        self.updateImage()
        self.lastPos = (self.x, self.y)
        self.x += self.xShift
        self.y += self.yShift

        # "Pre-move" to check if it is colliding with a wall, so we should undo the movement
        self.collisionRect.left += self.xShift  # move the collision rect to the future position
        self.collisionRect.bottom += self.yShift
        Interactive.update(self)  # check collisions
        self.collisionRect.left -= self.xShift  # return the collision rect to the current position
        self.collisionRect.bottom -= self.yShift

        self.lastPos = (self.x, self.y)

    def onCollisionEnter(self, collided):

        if isinstance(collided, Tile):
            self.x, self.y = self.lastPos
            self.objectsEnterCollision.remove(collided)

    def pillEffect(self):
        self.speed = self.speed * 0.5


class Player(Character, Subject):
    """
    Class that represents the playable character
    """""

    def __init__(self, position, speed=1, animationDelay=4):
        Subject.__init__(self)
        Character.__init__(self, 'character.png', 'coordMan.txt', [3, 3, 3, 3], position, (25, 29),
                           speed, animationDelay, 0)

        # We use a new rect that is placed at the bottom body-upper legs of the sprite to detect collisions
        legsRect = self.rect.copy()
        legsRect.inflate_ip(-5, -13)
        legsRect.bottom = self.rect.bottom - 2
        legsRect.left = self.rect.left + (self.rect.width - legsRect.width) / 2
        self.changeCollisionRect(legsRect)

        # Load the movement bindings from the configuration file
        self.MOVE_UP, self.MOVE_DOWN, self.MOVE_RIGHT, self.MOVE_LEFT = ConfManager().getPlayerMovementBinds()
        self.lastMovements = [IDLE]  # ordered sequence of movement keys pressed by the user (more info in move method)

        self.eventsEnabled = True

        self.hasPills = 0

    def increaseSpeed(self):
        self.speed *= 1.5
        self.animationDelay /= 1.5

    def disableEvents(self):
        self.eventsEnabled = False

        # Stop the player
        self.lastMovements = [IDLE]
        self.movement = IDLE

    def enableEvents(self):
        self.eventsEnabled = True

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

        # Remove from the list the key, we have to check if it is there in case another object got control of the events
        # and we did not capture the realising
        elif event.type == KEYUP:

            if event.key == self.MOVE_LEFT and LEFT in self.lastMovements:
                self.lastMovements.remove(LEFT)
            elif event.key == self.MOVE_RIGHT and RIGHT in self.lastMovements:
                self.lastMovements.remove(RIGHT)
            elif event.key == self.MOVE_UP and UP in self.lastMovements:
                self.lastMovements.remove(UP)
            elif event.key == self.MOVE_DOWN and DOWN in self.lastMovements:
                self.lastMovements.remove(DOWN)

    def events(self, events):

        if not self.eventsEnabled:
            self.movement = IDLE
            return

        for event in events:
            self.move(event)

    def update(self, time):

        self.movement = self.lastMovements[-1]  # the last key pressed by the user
        Character.update(self, time)

        self.notify()  # notify to draw the level properly

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
     


class Enemy(Character, Entity):

    def __init__(self, imageFile, coordFile, sheetDimension, position, playerGroup, scale, speed, animationDelay, updateByTime):
        Character.__init__(self, imageFile, coordFile, sheetDimension, position, scale, speed, animationDelay, updateByTime)
        Entity.__init__(self)
        Entity.setPlayer(self, playerGroup.sprites()[0], position)
        self.extrax, self.extray = (0, 0)
        
        self.addCollisionGroup(playerGroup)

    def updateObserver(self, subject):
        Entity.updateObserver(self, subject)
        self.rect.left += self.extrax
        self.rect.bottom += self.extray
    
    def onCollisionEnter(self, collided):

        if isinstance(collided, Tile):
            self.x, self.y = self.lastPos
            self.objectsEnterCollision.remove(collided)
        if isinstance(collided, Player):
            Director().pop()

class WalkingEnemy(Enemy):
    def __init__(self, imageFile, coordFile, sheetDimension, position, playerGroup, scale, speed, animationDelay, updateByTime, waypoints):
        Enemy.__init__(self, imageFile, coordFile, sheetDimension, position, playerGroup, scale, speed, animationDelay, updateByTime)
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
            self.posture = 0
        else:
            self.movement = RIGHT
            self.posture = 1
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
        self.extrax += self.vel[0]
        self.extray += self.vel[1]
        # self.rect.center = self.pos
        super().updateImage()
       

# -------------------------------------------------
# Basic enemy 0 class

class Basic0(Enemy, Entity):
    def __init__(self, position, playerGroup):
        # called constructor of father class
        Enemy.__init__(self, 'B0.png', 'coordBasic0.txt', [7], position, playerGroup, (32, 32), 0.3, 5, 0.5)


# -------------------------------------------------
# Basic enemy 1 class

class Basic1(WalkingEnemy, Entity):
    def __init__(self, position, waypoints, speed, playerGroup):
        # called constructor of father class
        WalkingEnemy.__init__(self, 'B1.1.png', 'coordBasic1.1.txt', [6,6], position, playerGroup, (32, 32), speed, 5, 0.5, waypoints)


# -------------------------------------------------
# Basic enemy 2 class

class Basic2(Enemy, Entity):
    def __init__(self, position, player, radius, playerGroup):
        # called constructor of father class
        self.radius=radius
        self.enemy=player
        Enemy.__init__(self, 'B2.png', 'coordBasic2.txt', [10], position, playerGroup, (148, 120), 0.3, 15, 0.5)

        

    def updateImage(self):
        self.timeToUpdateSprite -= 1

        # check if time between sprites updates

        self.pos = pygame.math.Vector2((self.x, self.y))
        self.target = (self.enemy.x, self.enemy.y)
        heading = self.target - self.pos
        distance = heading.length() 
        heading.normalize_ip()
        if distance <= self.radius:   
            if self.timeToUpdateSprite < 0:
                self.timeToUpdateSprite = self.animationDelay
                # update sprite
                self.subPosture += 1
                if self.subPosture >= len(self.sheetCoord[self.posture]):
                    self.subPosture = 0
                if self.subPosture < 0:
                    self.subPosture = len(self.sheetCoord[self.posture]) - 1
                self.image= pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][self.subPosture]), self.scale)
        else:
            # no movement is being done
            if self.movement == IDLE:
                self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.posture][0]), self.scale)
            

# -------------------------------------------------
# Normal enemy 2 

class Normal2(Enemy):
    "Normal2 enemy 3"
    def __init__(self, position, player, playerGroup):
        # called constructor of father class
        Enemy.__init__(self, 'N2.2.png', 'coordNormal2.2.txt', [3,3,3,3], position, playerGroup, (32, 50), 0.1, 5, 0)
        self.player = player

    def update(self, *args):
        super().update(*args)
        self.move(self.player, 300)

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
# Advanced enemy 2

class Advanced2(WalkingEnemy):
    def __init__(self, position, speed, player, orientation, playerGroup):
        # called constructor of father class
        self.enemy=player
        self.looking=orientation
        self.activation=False
        Enemy.__init__(self, 'A2.png', 'coordA2.txt', [3, 10, 8, 3, 10, 8], position, playerGroup, (32, 32), speed, 5, 0.5)

    def update(self, time): #FALTA HACER LA COLISIÓN
        if self.enemy.y == self.y or self.activation == True: #Player cross
            self.activation= True
            if self.enemy.x > self.x:
                self.movement=RIGHT
                self.looking=RIGHT
                self.x += self.speed
                self.rect.left = self.x
                super().updateImage()
            else:
                self.looking=LEFT
                self.movement=LEFT 
                self.x -= self.speed
                self.rect.left = self.x
                super().updateImage()
        else: super().updateImage() #Movimiento estático


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
