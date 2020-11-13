import os
import pygame
#quité el atributo tipo

class Casilla:
    def __init__(self, framePG, ruta):
        self.tipo = "estandar"
        self.imagen = "imagenes/baseZombie.png"
        self.framePG = framePG
        self.ruta = ruta
        self.dimCuadros = 100 #OJO que está alambrado
        self.personaje = object
        # ---------------------
        #image_path = os.path.join("data", "images")
        #self.image = pygame.image.load(os.path.join(image_path, filename)).convert_alpha()
        #self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
    def setPersonaje(self,personaje):
        self.personaje = personaje
    def getPersonaje(self):
        return self.personaje
    def setImagen(self,imagen):
        self.imagen = imagen
    def setTipo(self,tipo):
        self.tipo = tipo
    def getTipo(self):
        return self.tipo
    def dibujarCasilla(self, fila, columna):
        color = (28, 3, 107) 
        
        imagen = pygame.image.load(os.path.join(self.ruta, self.imagen)).convert_alpha()
        if self.tipo!="casillaAlien":
            imagen = pygame.transform.scale(imagen, (self.dimCuadros, self.dimCuadros))
        cuadro = pygame.draw.rect(self.framePG,
                        color,
                        [(1 + self.dimCuadros) * columna + 1,
                        (1 + self.dimCuadros) * fila + 1,
                        self.dimCuadros,
                        self.dimCuadros])                 
        if self.tipo != "estandar":
            self.framePG.blit(imagen, cuadro)
        pygame.display.flip()   

    def getTipo(self):
        return self.tipo;   
   

class Obstaculo(Casilla):
    def __init__(self, framePG, ruta, bloqueoIzq, bloqueoDer, bloqueoArr, bloqueoAba):
        super().__init__(framePG, ruta)
        self.tipo = "obstaculo"
        self.bloqueoIzq = bloqueoIzq
        self.bloqueoDer = bloqueoDer
        self.bloqueoArr = bloqueoArr
        self.bloqueoAba = bloqueoAba
        self.imagen = "imagenes/obstaculo.png"

    def setBloqueoIzq(self, bloqueoIzq):
        self.bloqueoIzq #preguntar 

    def consultarBloqueoIzq(self, bloqueoIzq):
        return self.bloqueoIzq        


class Base(Casilla):
    def __init__(self, framePG, ruta, conquistada, aliada):
        super().__init__(framePG, ruta)
        self.tipo = "base"
        self.conquistada = conquistada
        self.aliada = aliada
        self.imagen = self.definirBase()

    def definirBase(self):
        if self.aliada:
            base = "imagenes/baseAlien.png"
        else:
            base = "imagenes/baseZombie.png"
        return base

    def evaluarConquistada(self):
        pass


class SpawningPoint(Casilla): #Asumí el atributo zombi como el tipo, (int)
    def __init__(self, framePG, ruta, zombi):
        super().__init__(framePG, ruta)
        self.tipo = "sp"
        self.zombi = zombi
        self.imagen = "imagenes/spwnPt.png"
        #self.dimCuadros = 100 #OJO que está alambrado

    def crearZombi(self):
        pass

    
