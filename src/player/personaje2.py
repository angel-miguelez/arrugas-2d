# -*- coding: utf-8 -*-

# -------------------------------------------------
# Importar las librerías
# -------------------------------------------------
from utils.resourcesmanager import *
import itertools
from utils.observer import Subject

# movements
left = 0
right = 1
up = 2
down = 3
stop = 4
diagUpLeft = 5
diagUpRight = 6
diagDownLeft = 7
diagDownRight = 8

#const
diag = 0.707

# -------------------------------------------------
# Character class
# -------------------------------------------------

class Character(pygame.sprite.Sprite):
    "Character"

    def __init__(self, imageFile, coordFile, imageNum, coordScreen, scale, speed, animationDelay, updateByTime, walls=None):
    # imageFile -> file with image data
    # coordFile -> File with all the coordinades of the sprites from imageFile
    # imageNUm -> array with the number of diferent sprites. ex: [4, 4] 2 positions with 4 different sprites each position
    # coordScreen -> coordinates on screen where sprite is initialized
    # scale -> size of the sprites
    # speed 
    # animationDelay -> delay on each movement of the characters
    # updateByTime -> if sprite is updated every moment(basic0) or updated while moving(player) 
    

        pygame.sprite.Sprite.__init__(self)
        self.walls = walls

        # load sheet
        self.sheet = ResourcesManager.loadImage(imageFile, -1)
        self.sheet = self.sheet.convert_alpha()
        # movement realized
        self.movement = stop
        # where's looking
        self.looking = down

        # reading coords from file
        data = ResourcesManager.loadCoordFile(coordFile)
        data = data.split()
        self.positionNum = 1
        self.imagePositionNum = 0
        cont = 0
        self.sheetCoord = []
        numLines = len(imageNum)
        for line in range(0, numLines):
            self.sheetCoord.append([])
            tmp = self.sheetCoord[line]
            for position in range(1, imageNum[line]+1):
                tmp.append(pygame.Rect((int(data[cont]), int(data[cont+1])), (int(data[cont+2]), int(data[cont+3]))))
                cont += 4

        # delay while changing positions
        self.movementDelay = 0;

        # initial position
        self.positionNum = left

        # rectangle tam
        self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.positionNum][self.imagePositionNum]), scale)
        self.rect = self.image.get_rect()

        # X and Y coordinates on screen
        self.positionX = coordScreen[0]
        self.positionY = coordScreen[1]
        self.rect.left = self.positionX
        self.rect.bottom = self.positionY

        # player speed and animation delay(smooth the sprite changes)
        self.animationDelay = animationDelay
        self.playerSpeed = speed
        self.updateByTime = updateByTime
        self.scale = scale

        # update sprites
        self.updatePosition()

        self.lastHor = 0
        self.lastVer = 0
        self.lastPos = (self.positionX, self.positionY)



    def updatePosition(self):
        self.movementDelay -= 1
        # check if time between sprites updates
        if (self.movementDelay < 0):
            self.movementDelay = self.animationDelay
            # update sprite
            self.imagePositionNum += 1
            if self.imagePositionNum >= len(self.sheetCoord[self.positionNum]):
                self.imagePositionNum = 0;
            if self.imagePositionNum < 0:
                self.imagePositionNum = len(self.sheetCoord[self.positionNum])-1
            self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.positionNum][self.imagePositionNum]), self.scale)
            # watching left
            if self.looking == left:
                self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.positionNum][self.imagePositionNum]), self.scale)
            #  watching right
            elif self.looking == right:
                 self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.positionNum][self.imagePositionNum]), self.scale)
            # watching up
            elif self.looking == up:
                self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.positionNum][self.imagePositionNum]), self.scale)
            # watching down
            elif self.looking == down:
                self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.positionNum][self.imagePositionNum]), self.scale)
            # no movement is being done
            if(self.updateByTime == 0):
                if self.movement == stop:
                    self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.positionNum][0]), self.scale)


    def update(self, time):
        """
        For now i'll leave uncomentted, but i've discovered why the movement
        was so scuffed, we were updating both the player position and map position
        depending on the player input wich resulted in some strange interaction.
        When the player was moving downwards, the player sprite moved faster than
        the map which created an offset between the map and the player position, this
        resulted in the map and player going off-screen.
        The way to fix it would be commenting or eliminating the lines were we update
        the 'self.rect' position.
        """

        self.lastHor = 0
        self.lastVer = 0

        # moving left
        if self.movement == left:
            # looking left
            self.looking = left
            self.positionNum = 0
            self.lastHor = - int(self.playerSpeed * time)
        # moving right
        elif self.movement == right:
            # looking right
            self.looking = right
            self.positionNum = 1
            self.lastHor = int(self.playerSpeed * time)
        # moving up
        elif self.movement == up:
            # looking up
            self.looking = up
            self.positionNum = 2
            self.lastVer = - int(self.playerSpeed * time)
        # moving down
        elif self.movement == down:
            # looking down
            self.looking = down
            self.positionNum = 3
            self.lastVer = int(self.playerSpeed * time)
        elif self.movement == diagUpLeft:
            # looking down
            self.looking = up
            self.lastVer = - int(diag * self.playerSpeed * time)
            self.lastHor = -int(diag * self.playerSpeed * time)
            self.positionNum = 2
        elif self.movement == diagUpRight:
            # looking down
            self.looking = up
            self.lastVer = - int(diag * self.playerSpeed * time)
            self.lastHor = int(diag * self.playerSpeed * time)
            self.positionNum = 2
        elif self.movement == diagDownLeft:
            # looking down
            self.looking = down
            self.lastVer = int(diag * self.playerSpeed * time)
            self.lastHor = - int(diag * self.playerSpeed * time)
            self.positionNum = 3
        elif self.movement == diagDownRight:
            # looking down
            self.looking = down
            self.lastVer = int(diag * self.playerSpeed * time)
            self.lastHor = int(diag * self.playerSpeed * time)
            self.positionNum = 3
        # while stopped not changes are done

        # update
        self.updatePosition()
        self.lastPos = (self.positionX, self.positionY)
        self.positionX += self.lastHor
        self.positionY += self.lastVer

    def pillEffect(self):
        self.playerSpeed=self.playerSpeed*0.5
        
# -------------------------------------------------
# Player class
def _collideCollisionRect(left, right):
    return left.legsRect.colliderect(right.rect)

class Player(Character, Subject):
    "Main character"
    def __init__(self, pos, walls):
        Subject.__init__(self)

        # called constructor of father class
        Character.__init__(self, 'character.png', 'coordMan.txt', [3, 3, 3, 3], [
                           pos[0], pos[1]], (30, 30), 0.1, 4, 0, walls)
        self.eventsEnabled = True
        self.hasPills = 0

        self.legsRect = self.rect.copy()
        self.legsRect.inflate_ip(-5, -13)
        self.legsRect.bottom = self.rect.bottom - 2
        self.legsRect.left = self.rect.left + (self.rect.width - self.legsRect.width) / 2

    def increaseSpeed(self):
        self.playerSpeed *= 1.5

    def disableEvents(self):
        self.eventsEnabled = False

    def enableEvents(self):
        self.eventsEnabled = True

        # move function
    def move(self, toggledKeys, upControl, downControl, leftControl, rightControl):

        if not self.eventsEnabled:
            self.movement = stop
            return

        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if (toggledKeys[upControl] and toggledKeys[leftControl]):
            self.movement = diagUpLeft
        elif (toggledKeys[upControl] and toggledKeys[rightControl]):
            self.movement = diagUpRight
        elif (toggledKeys[downControl] and toggledKeys[leftControl]):
            self.movement = diagDownLeft
        elif (toggledKeys[downControl] and toggledKeys[rightControl]):
            self.movement = diagDownRight
        elif toggledKeys[upControl]:
            self.movement = up
        elif toggledKeys[leftControl]:
            self.movement = left
        elif toggledKeys[rightControl]:
            self.movement = right
        elif toggledKeys[downControl]:
            self.movement = down
        else:
            self.movement = stop

        # self.notify()

    def update(self, time):
        super().update(time)
        self.notify()

        collidedHor, collidedVer = (False, False)
        collided = pygame.sprite.spritecollide(self, self.walls, False, _collideCollisionRect)
        if len(collided) > 0:

            for sprite in collided:
                difference = abs(self.legsRect.center[1] - sprite.rect.center[1])
                maxDifference = self.legsRect.height / 2 + sprite.rect.height / 2
                if maxDifference - difference < 10:
                    collidedVer = True

                difference = abs(self.legsRect.center[0] - sprite.rect.center[0])
                maxDifference = self.legsRect.width / 2 + sprite.rect.width / 2
                if maxDifference - difference < 10:
                    collidedHor = True

        if collidedHor:
            self.positionX = self.lastPos[0]
        if collidedVer:
            self.positionY = self.lastPos[1]

        self.lastPos = (self.positionX, self.positionY)
        self.notify()

    def getPos(self):
        return (self.positionX, self.positionY)

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
        self.rect.bottom = self.positionY
        self.rect.left = self.positionX

class WalkingEnemy(Enemy):
    def __init__(self, imageFile, coordFile, imageNum, coordScreen, scale, speed, animationDelay, updateByTime, waypoints):
        Character.__init__(self,imageFile, coordFile, imageNum, coordScreen, scale, speed, animationDelay, updateByTime);
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2((self.positionX, self.positionY))
        self.target_radius = 20
        self.waypoints = itertools.cycle(waypoints)
        self.target = next(self.waypoints)
        self.orientationvector=itertools.cycle((right,left))
        self.orientation=next(self.orientationvector)

    def update(self, time):
        # A vector pointing from self to the target.
        heading = self.target - self.pos
        if(heading[0] > 0):
            self.movement = left
            self.looking = left
            self.positionNum = 0
        else:
            self.movement = right
            self.movement = right
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
            self.vel = heading * (distance / self.target_radius * self.playerSpeed)
        else:  # Otherwise move with max_speed.
            self.vel = heading * self.playerSpeed

        self.pos += self.vel
        self.rect.center = self.pos
        super().updatePosition()
       

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
        

    def updatePosition(self):
        self.movementDelay -= 1
        # check if time between sprites updates

        self.pos = pygame.math.Vector2((self.positionX, self.positionY))
        self.target = (self.enemy.positionX, self.enemy.positionY)
        heading = self.target - self.pos
        distance = heading.length() 
        heading.normalize_ip()
        if distance <= self.radius:   
            if (self.movementDelay < 0):
                self.movementDelay = self.animationDelay
                # update sprite
                self.imagePositionNum += 1
                if self.imagePositionNum >= len(self.sheetCoord[self.positionNum]):
                    self.imagePositionNum = 0;
                if self.imagePositionNum < 0:
                    self.imagePositionNum = len(self.sheetCoord[self.positionNum])-1
                self.image= pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.positionNum][self.imagePositionNum]), self.scale)
        else:
            # no movement is being done
            if self.movement == stop:
                self.image = pygame.transform.scale(self.sheet.subsurface(self.sheetCoord[self.positionNum][0]), self.scale)
            

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
        if (abs(self.positionX - player.positionX) < area) and (abs(self.positionY - player.positionY) < area):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
            if ((self.positionX - player.positionX) == 0) and ((self.positionY - player.positionY) == 0):
                 self.movement = stop
            elif ((self.positionX - player.positionX) == 0) and ((self.positionY - player.positionY) > 0):
                 self.movement = up
            elif ((self.positionX - player.positionX) == 0) and ((self.positionY - player.positionY) < 0):
                 self.movement = down
            elif ((self.positionX - player.positionX) < 0) and ((self.positionY - player.positionY) == 0):
                 self.movement = right
            elif ((self.positionX - player.positionX) > 0) and ((self.positionY - player.positionY) == 0):
                 self.movement = left
            elif ((self.positionX - player.positionX) < 0) and ((self.positionY - player.positionY) < 0):
                 self.movement = down
            elif ((self.positionX - player.positionX) > 0) and ((self.positionY - player.positionY) > 0):
                 self.movement = up
            elif ((self.positionX - player.positionX) < 0) and ((self.positionY - player.positionY) > 0):
                 self.movement = right
            elif ((self.positionX - player.positionX) > 0) and ((self.positionY - player.positionY) < 0):
                 self.movement = left        
        else:
             self.movement = stop        



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
