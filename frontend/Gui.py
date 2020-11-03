import os, sys;
import random
import pygame
from Clases.Casilla import *
from Clases.Personaje import Alien
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
        posicion = pygame.mouse.get_pos()
        columna = posicion[0] // ( self.dimCuadros + 1) #width
        fila = posicion[1] // ( self.dimCuadros + 1) #altura
        self.matriz[fila][columna] = 1 #Cambiarle el color a la casilla
        print("Posición ", posicion, "Coordenadas en nuestra cuadrícula: ", fila, columna)
        
    def manejarEventos(self):
        while not self.terminar:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.salir()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.getCasillaSeleccionada()
            self.dibujarCasillas()
            pygame.display.update()
    
class Boton():   
    def __init__(self,x,y,ancho,alto,texto,screen):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.textoBoton = texto
        self.rectangulo = pygame.Rect(x,y,ancho,alto)
        self.screen = screen
        self.fuente = pygame.font.SysFont("Arial",25)
    def dibujarBoton(self):
        pygame.draw.rect(self.screen,(30, 139, 176),self.rectangulo,0)#variable de la pantalla, (colores RGB), rectangulo, borde
        texto = self.fuente.render(self.textoBoton,True,((random.randrange(0, 100), random.randrange(0, 100), random.randrange(0, 100))))
        self.screen.blit(texto, (self.x+((self.ancho-texto.get_width())/2),self.y+(self.alto-texto.get_height())/2))#centra el texto en el boton
    def verificarPresionado(self):
        if self.rectangulo.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False
        
class Vestibulo(pygame.sprite.Sprite):
    def __init__(self, titulo, dimensiones):
        pygame.sprite.Sprite.__init__(self) #herencia  
        #self.colorFondo = colorFondo
        self.framePG =  pygame.display.set_mode(dimensiones)
        self.ruta = os.path.dirname(__file__)#importante!! captura la ruta de este archivo sin importar la computadora
        self.alien1 = Alien("Andrómeda",self.ruta,"imagenes/alien1.png")
        self.alien2 = Alien("Osa Mayor",self.ruta,"imagenes/alien2.png")
        self.alien3 = Alien("Orión",self.ruta,"imagenes/alien3.png")
        self.botonAndromeda = Boton(112, 407,120,50,"Seleccionar",self.framePG)
        self.botonOsaMayor = Boton(444, 407,120,50,"Seleccionar",self.framePG)
        self.botonOrion = Boton(760, 407,120,50,"Seleccionar",self.framePG)
        self.posX  =100
        self.posY = 50
        pygame.display.set_caption(titulo)
        self.terminar = False
        self.mantenerEscucha()
        self.alienSeleccionado;#atributo para el alien seleccionado
    def setAlienSeleccionado(self,alien):
        self.alienSeleccionado = alien;
    def getAlienSeleccionado(self):
        return self.alienSeleccionado;
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
        if self.botonAndromeda.verificarPresionado():
            self.mostrarHabilidades(self.alien1)
            self.setAlienSeleccionado(self.alien1);#asigna el personaje seleccionado
        elif self.botonOsaMayor.verificarPresionado():
            self.mostrarHabilidades(self.alien2)
            self.setAlienSeleccionado(self.alien2);
        elif self.botonOrion.verificarPresionado():
            self.mostrarHabilidades(self.alien3)
            self.setAlienSeleccionado(self.alien3);
        else:
            print(posicion)
    def mostrarHabilidades(self,palien):
        texto = palien.obtenerHabilidades()
##        fuente = pygame.font.Font(None,30)
##        mensaje = fuente.render(texto, 0, (200, 60, 80))
##        self.framePG.blit(mensaje, (0, 0))
        print(texto)
    def dibujarBotones(self):
        self.botonAndromeda.dibujarBoton()
        self.botonOsaMayor.dibujarBoton()
        self.botonOrion.dibujarBoton()
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
            self.dibujarBotones()
            pygame.display.update()         

class Inicio(pygame.sprite.Sprite):
    def __init__(self, titulo, dimensiones):
        pygame.sprite.Sprite.__init__(self) #herencia  
        #self.colorFondo = colorFondo
        pygame.init() 
        self.ruta = os.path.dirname(__file__)
        self.imgZombie = pygame.image.load(os.path.join(self.ruta, "imagenes/titulo.png"))
        self.imgGalaxy = pygame.image.load(os.path.join(self.ruta, "imagenes/titulo2.png"))
        self.posX  =100
        self.posY = 50
        self.framePG =  pygame.display.set_mode(dimensiones)
        pygame.display.set_caption(titulo)
        self.color = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))
        self.dimensiones = dimensiones
        self.font = pygame.font.Font ('freesansbold.ttf', 32)
        self.terminar = False
        self.mantenerEscucha()

    def getDimensiones(self):
        return self.dimensiones
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

    def mantenerEscucha(self):
        while not self.terminar:
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    self.salir()
                elif eventos.type == pygame.KEYDOWN:
                    self.jugar()
            #framePG.blit(self.imgTitulo,(100,100))
            self.color = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))
            self.insertarImgs()
            self.insertarTxt()
            pygame.display.update()

class Main():
    if __name__ == "__main__":
        app = Inicio("Zombie Galaxy", (1012, 600))
        
