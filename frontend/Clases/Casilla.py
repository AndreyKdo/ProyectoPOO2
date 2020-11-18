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
    def getImagen(self):
        return self.imagen
    def setTipo(self,tipo):
        self.tipo = tipo
    def getTipo(self):
        return self.tipo
    def dibujarCasilla(self, fila, columna):
        color = (28, 3, 107) 
        
        imagen = pygame.image.load(os.path.join(self.ruta, self.imagen)).convert_alpha()
        
        if (self.tipo != "casillaAlien") and (self.tipo != "casillaZombi"):
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
    def __init__(self, framePG, ruta, a, b, c, d): #
        super().__init__(framePG, ruta)
        self.tipo = "sp"
        self.bloqueoIzq = d
        self.bloqueoDer = b
        self.bloqueoArriba = a
        self.bloqueoAbajo = c
        self.imagen = self.definirImg()

    def definirImg(self):
        bloqueos = [self.bloqueoArriba, self.bloqueoDer, self.bloqueoAbajo, self.bloqueoIzq]
        hayBloqueos = False #suponemos que el tipo de SpPt es estándar (sin líneas rojas = no hay bloqueos)
        strImg = "imagenes/spwn"

        for i in range(len(bloqueos)):
            if bloqueos[i] == True: #analizamos los bordes, y si se encuentra un verdadero para un borde
                hayBloqueos = True #desmentimos la preposición de que no había, (sí hay bloqueos)

        if hayBloqueos: #si hay bloqueos, armamos el string de la img para dicha combinación de bloqueos
            if self.bloqueoArriba:
                strImg += "A"
            if self.bloqueoDer:
                strImg += "B"
            if self.bloqueoAbajo:
                strImg += "C"
            if self.bloqueoIzq:
                strImg += "D" #ACA
            strImg += ".jpg"
        else: #si nunca hubo bloqueos, usamos nuestra imagen estándar que no tiene lineas rojas
            strImg = "imagenes/spwnPt.jpg"
        print(strImg)
        return strImg

    def getImagen(self):
        return self.imagen

    def getBloqueoIzq(self):
        return self.bloqueoIzq

    def getBloqueoDer(self):
        return self.bloqueoDer

    def getBloqueoAbajo(self):
        return self.bloqueoAbajo

    def getBloqueoArriba(self):
        return self.bloqueoArriba



    
