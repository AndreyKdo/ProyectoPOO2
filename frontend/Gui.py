import pygame;
import os, sys;
import tkinter as tk;
import random
from backend.Personaje import Alien
class Casilla:
    def __init__(self, framePG, tipo):
        self.tipo = ""
        self.framePG = framePG
        # ---------------------
        #image_path = os.path.join("data", "images")
        #self.image = pygame.image.load(os.path.join(image_path, filename)).convert_alpha()
        #self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
   
class Obstaculo(Casilla):
    def __init__(self, tipo, bloqueoIzq, bloqueoDer, bloqueoArr, bloqueoAba):
        super().__init__(self, tipo)
        self.bloqueoIzq = bloqueoIzq
        self.bloqueoDer = bloqueoDer
        self.bloqueoArr = bloqueoArr
        self.bloqueoAba = bloqueoAba
        self.imgObst = 'obstaculo.png'

    def setBloqueoIzq(self, bloqueoIzq):
        self.bloqueoIzq #preguntar 

    def consultarBloqueoIzq(self, bloqueoIzq):
        return self.bloqueoIzq

class Base(Casilla):
    def __init__(self, tipo, conquistada, aliada):
        super().__init__(self, tipo)
        self.imgBaseAliada = 'baseZombie.png'
        self.imgBaseEnemiga = 'baseAlien.png'

    def evaluarConquistada(self):
        pass

class SpawningPoint(Casilla):
    def __init__(self, tipo, zombi):
        super().__init__(self, tipo)
        #self.zombi = Zombi()
        self.imgSpPt = 'spwnPt.png'
        #self.dimCuadros = 100 #OJO que está alambrado

    def crearZombi(self):
        pass

class CampoBatalla(pygame.sprite.Sprite):
    def __init__(self, titulo, dimCuadros, dimFrame, colorCuadros, colorLineas):
        pygame.sprite.Sprite.__init__(self) #herencia
        self.titulo = titulo
        self.dimCuadros = int(dimCuadros) #100
        self.dimFrame = dimFrame; #(1012, 600);
        self.colorCuadros = colorCuadros; #azul = (24, 22, 67);
        self.colorLineas = colorLineas; #morado = (88, 40, 165);
        self.matriz = self.generarMatriz()
        self.imagen = ""
        self.framePG = self.dibujarCampoBatalla()
        
        #self.casilla = Casilla(self.framePG, self.matriz, "", self.dimCuadros)
        self.terminar =False
        self.manejarEventos()

    def generarMatriz(self):      
        matrizCuadriculada = []
        for fila in range(6):
            matrizCuadriculada.append([])
            for columna in range(10):
                if fila== 5 and columna == 0: 
                    matrizCuadriculada[fila].append(list(["base", False, True])) 
                elif fila== 5 and columna == 9:
                    matrizCuadriculada[fila].append(list(["base", False, False])) 
                elif (fila== 4 and columna == 9) or (fila== 5 and columna == 8): 
                    matrizCuadriculada[fila].append(list(["sp", ["zombi1", "zombi2", "zombi3"]]))
                else:
                    matrizCuadriculada[fila].append(0)  #Casilla() vacía
        return list(matrizCuadriculada)

    def dibujarCasillaEstandar(self, fila, columna):
        color = self.colorCuadros #azul
        pygame.draw.rect(self.framePG,
                        color,
                        [(1 + self.dimCuadros) * columna + 1,
                        (1 + self.dimCuadros) * fila + 1,
                        self.dimCuadros,
                        self.dimCuadros])
        pygame.display.flip()

    def dibujarCasillaBase(self, fila, columna):
        color = (0, 0, 0) #self.imgBaseEnemiga
        pygame.draw.rect(self.framePG,
                        color,
                        [(1 + self.dimCuadros) * columna + 1,
                        (1 + self.dimCuadros) * fila + 1,
                        self.dimCuadros,
                        self.dimCuadros])
        pygame.display.flip()

    def dibujarCasillaObs(self, fila, columna):
        color = (0, 255, 0) #setear self.imgObst
        pygame.draw.rect(self.framePG,
                        color,
                        [(1 + self.dimCuadros) * columna + 1,
                        (1 + self.dimCuadros) * fila + 1,
                        self.dimCuadros,
                        self.dimCuadros])
        pygame.display.flip()

    def dibujarCasillaSpPt(self, fila, columna):
        color = (255, 0, 0) #setear self.imgSpPt
        pygame.draw.rect(self.framePG,
                        color,
                        [(1 + self.dimCuadros) * columna + 1,
                        (1 + self.dimCuadros) * fila + 1,
                        self.dimCuadros,
                        self.dimCuadros])
        pygame.display.flip()

    def dibujarCasillas(self):
        for fila in range( len(self.matriz)):
            for columna in range (len(self.matriz[fila])):
                if (self.matriz[fila][columna]) != 0:
                    self.dibujarCasillaObs(fila, columna)
                    #if self.matriz[fila][columna][0] == "sp":
                        #self.dibujarCasillaSpPt(fila, columna)
                    #elif self.matriz[fila][columna][0] == "obstaculo":
                        #self.dibujarCasillaObs(fila, columna)
                    #elif self.matriz[fila][columna][0] == "base":
                        #self.dibujarCasillaBase(fila, columna)
                else:
                    self.dibujarCasillaEstandar(fila, columna)
    def salir(self):
        pygame.quit()
        sys.exit()
        self.terminar = True


    def dibujarCampoBatalla(self):
        framePG =  pygame.display.set_mode(self.dimFrame)
        framePG.fill(self.colorLineas)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.titulo)
        #pygame.display.flip()
        pygame.display.update() 
        return framePG

    def getCasillaSeleccionada(self):
        posicion = pygame.mouse.get_pos()#captura el lugar donde se da click
        columna = posicion[0] // ( self.dimCuadros + 1) #width
        fila = posicion[1] // ( self.dimCuadros + 1) #altura
        self.matriz[fila][columna] = 1 #Cambiarle el color a la casilla
        print("Posición ", posicion, "Coordenadas en nuestra cuadrícula: ", fila, columna)
        
    def manejarEventos(self):#mantiene escucha
        while not self.terminar:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                elif evento.type == pygame.KEYDOWN:#enter
                    if evento.key == pygame.K_ESCAPE:#escape para salir
                        self.salir()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.getCasillaSeleccionada()
            self.dibujarCasillas()
            pygame.display.update()

class PersonajeAlien():
    def __init__(self,ruta,imagen,nombre):
        self.imgAlien = pygame.image.load(os.path.join(ruta, imagen))
        self.alien = Alien(nombre)
        self.imprimirAlien()
    def imprimirAlien(self):
        print(self.alien.getNombre())
    def getImagen(self):
        return self.imgAlien

class Vestibulo(pygame.sprite.Sprite):
    def __init__(self, titulo, dimensiones):
        pygame.sprite.Sprite.__init__(self) #herencia  
        #self.colorFondo = colorFondo
        self.ruta = os.path.dirname(__file__)#importante!! captura la ruta de este archivo sin importar la computadora

        self.alien1 = PersonajeAlien(self.ruta,"alien1.png","Andrómeda")
        self.alien2 = PersonajeAlien(self.ruta,"alien2.png","Osa Mayor")
        self.alien3 = PersonajeAlien(self.ruta,"alien3.png","Orión")
        self.posX  =100
        self.posY = 50
        self.framePG =  pygame.display.set_mode(dimensiones)
        pygame.display.set_caption(titulo)
        self.terminar = False
        self.mantenerEscucha()

    def insertarImgs(self):
        self.framePG.blit(self.alien1.getImagen(), (self.posX, self.posY))
        self.framePG.blit(self.alien2.getImagen(), (self.posX+300, self.posY+100))
        self.framePG.blit(self.alien3.getImagen(), (self.posX+600, self.posY+100))

    def jugar(self):
        self.terminar = True
        campoBatalla= CampoBatalla("Galaxia Zombi", 100, (1012, 600), (24, 22, 67), (88, 40, 165));
       
    def salir(self):
        #pygame.quit()
        #sys.exit()
        self.terminar = True
    def getPersonajeSeleccionado(self):
        posicion = pygame.mouse.get_pos()#captura el lugar donde se da click
        print(posicion)
    def botones(self):
        pass
        
    def mantenerEscucha(self):#keep listening, esperando eventos
        while not self.terminar:
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    self.salir()
                elif eventos.type == pygame.KEYDOWN:
                    self.jugar()#metodo de jugar
                elif eventos.type == pygame.MOUSEBUTTONDOWN:
                    self.getPersonajeSeleccionado()
            #framePG.blit(self.imgTitulo,(100,100))
            self.insertarImgs()
            self.botones()
            pygame.display.update()         

class Inicio(pygame.sprite.Sprite):
    def __init__(self, titulo, dimensiones):
        pygame.sprite.Sprite.__init__(self) #herencia  
        #self.colorFondo = colorFondo
        pygame.init() 
        self.ruta = os.path.dirname(__file__)
        self.imgZombie = pygame.image.load(os.path.join(self.ruta, "titulo.png"))
        self.imgGalaxy = pygame.image.load(os.path.join(self.ruta, "titulo2.png"))
        self.posX  =100
        self.posY = 50
        self.framePG =  pygame.display.set_mode(dimensiones)
        pygame.display.set_caption(titulo)
        self.color = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))
        self.dimensiones = dimensiones
        self.font = pygame.font.Font ('freesansbold.ttf', 32)
        self.terminar = False
        self.mantenerEscucha()

    def insertarTxt(self):
        self.texto= self.font.render("Presione enter para comenzar", True, (self.color), (0,0,0))
        textRect = self.texto.get_rect()  
        textRect.center = (self.dimensiones[0] // 2, self.dimensiones[1] //2 +150) 
        self.framePG.blit(self.texto, textRect) 

    def insertarImgs(self):
        self.framePG.blit(self.imgZombie, (self.posX, self.posY))
        self.framePG.blit(self.imgGalaxy, (self.posX+200, self.posY+100))

    def jugar(self):
        self.terminar = True
        Vestibulo("Personaje", (1012, 600))
        
    def salir(self):
        #pygame.quit()
        #sys.exit()
        self.terminar = True

    def mantenerEscucha(self):#keep listening, esperando eventos
        while not self.terminar:
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    self.salir()
                elif eventos.type == pygame.KEYDOWN:#enter, llama a jugar
                    self.jugar()
            #framePG.blit(self.imgTitulo,(100,100))
            self.color = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))
            self.insertarImgs()
            self.insertarTxt()
            pygame.display.update()

class Main():
    if __name__ == "__main__":
        app = Inicio("Zombie Galaxy", (1012, 600))



