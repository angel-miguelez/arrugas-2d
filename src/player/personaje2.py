# -*- coding: utf-8 -*-

# -------------------------------------------------
# Importar las librerías
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *

# movements
left = 0
right = 1
up = 2
down = 3
stop = 4


#playerSpeed = 0.2 # Pixeles por milisegundo
#animationDelay = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura


# -------------------------------------------------
# Character class
# -------------------------------------------------

class Character(pygame.sprite.Sprite):
    "Character"

    def __init__(self, imageFile, coordFile, imageNum, coordScreen, scale, speed, animationDelay, updateByTime):
    # imageFile -> file with image data
    # coordFile -> File with all the coordinades of the sprites from imageFile
    # imageNUm -> array with the number of diferent sprites. ex: [4, 4] 2 positions with 4 different sprites each position
    # coordScreen -> coordinates on screen where sprite is initialized
    # scale -> size of the sprites
    # speed 
    # animationDelay -> delay on each movement of the characters
    # updateByTime -> if sprite is updated every moment(basic0) or updated while moving(player) 
    
    
    
        pygame.sprite.Sprite.__init__(self);
        # load sheet
        self.sheet = GestorRecursos.CargarImagen(imageFile, -1)
        self.sheet = self.sheet.convert_alpha()
        # movement realized
        self.movement = stop
        # where's looking
        self.looking = down

        # reading coords from file
        data = GestorRecursos.CargarArchivoCoordenadas(coordFile)
        data = data.split()
        self.positionNum = 1;
        self.imagePositionNum = 0;
        cont = 0;
        self.sheetCoord = [];
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
        self.rect = pygame.Rect(100,100,self.sheetCoord[self.positionNum][self.imagePositionNum][2],self.sheetCoord[self.positionNum][self.imagePositionNum][3])

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
        # moving left
        if self.movement == left:
            # looking left
            self.looking = left
            # update screen coordinates
            self.positionX -= (int)(self.playerSpeed * time)
            self.rect.left = self.positionX
            self.positionNum = 0
        # moving right
        elif self.movement == right:
            # looking right
            self.looking = right
            # update screen coordinates
            self.positionX += (int)(self.playerSpeed * time)
            self.rect.left = self.positionX
            self.positionNum = 1
        # moving up
        elif self.movement == up:
            # looking up
            self.looking = up
            # update screen coordinates
            self.positionY -= (int)(self.playerSpeed * time)
            self.rect.bottom = self.positionY
            self.positionNum = 2
        # moving down
        elif self.movement == down:
            # looking down
            self.looking = down
            # update screen coordinates
            self.positionY += (int)(self.playerSpeed * time)
            self.rect.bottom = self.positionY
            self.positionNum = 3
        # while stopped not changes are done
        # update
        self.updatePosition()
        return
        
# -------------------------------------------------
# Player class

class Player(Character):
    "Main character"
    def __init__(self):
        # called constructor of father class
        Character.__init__(self, 'old_man.png', 'coordMan.txt', [3,3,3,3],[300, 100], (32,32), 0.3, 1, 0);

        #move function
    def move(self,toggledKeys, upControl, downControl, leftControl, rightControl):

        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if toggledKeys[upControl]:
            self.movement = up
        elif toggledKeys[leftControl]:
            self.movement = left
        elif toggledKeys[rightControl]:
            self.movement = right
        elif toggledKeys[downControl]:
            self.movement = down
        else:
            self.movement = stop

# -------------------------------------------------
# Basic enemy 0 class

class Basic0(Character):
    "Main character"
    def __init__(self):
        # called constructor of father class
        Character.__init__(self, 'Worm Sprite Sheet.png', 'coordBasic0.txt', [7],[100, 100], (32,32), 0.3, 5, 1);



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
    basic0 = Basic0()
    
    # Creamos el grupo de Sprites de jugadores
    grupoJugadores = pygame.sprite.Group( jugador1, basic0 )


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


        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        jugador1.move(toggledKeys, K_UP, K_DOWN, K_LEFT, K_RIGHT)



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
