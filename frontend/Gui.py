import os, sys;
import random
import pygame
from Clases.Casilla import *
from Clases.Personaje import Alien

class Boton():   
    def __init__(self,x,y,ancho,alto,texto, color, screen):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.textoBoton = texto
        self.color = color
        self.rectangulo = pygame.Rect(x,y,ancho,alto)
        self.screen = screen
        self.fuente = pygame.font.SysFont("Arial",25)
        self.mousePos = pygame.mouse.get_pos()
        
        
    def dibujarBoton(self):
        pygame.draw.rect(self.screen, self.color, self.rectangulo, 0)#variable de la pantalla, (colores RGB, 30, 139, 176), rectangulo, borde
        texto = self.fuente.render(self.textoBoton,True,((random.randrange(0, 100), random.randrange(0, 100), random.randrange(0, 100))))
        self.screen.blit(texto, (self.x+((self.ancho-texto.get_width())/2),self.y+(self.alto-texto.get_height())/2))#centra el texto en el boton
        
    def verificarPresionado(self, posicion):
        if self.rectangulo.collidepoint(posicion):
            return True
        else:
            return False

    def getTxt(self):
        return self.textoBoton

    def cambiarColorBtn(self, nuevoColor):
        self.color = nuevoColor
        
class CampoBatalla(pygame.sprite.Sprite):
    def __init__(self, titulo, dimCuadros, dimFrame, colorCuadros, colorLineas):
        pygame.sprite.Sprite.__init__(self) #herencia
        self.titulo = titulo
        self.dimCuadros = int(dimCuadros) #100
        self.dimFrame = dimFrame; #(1012, 600);
        self.colorCuadros = colorCuadros; #azul = (24, 22, 67);
        self.colorLineas = colorLineas; #morado = (88, 40, 165)
        self.ruta = os.path.dirname(__file__)
        self.framePG = self.dibujarCampoBatalla()
        self.matriz = self.generarMatriz()
        self.btnCurar = Boton(1153, 46,40,50, "Curar",(155, 155, 155), self.framePG)#self.crearBotones()
        #self.casilla = Casilla(self.framePG, self.matriz, "", self.dimCuadros)
        self.terminar =False
        self.manejarEventos()
    def llamarCurar(self):
        
    def generarMatriz(self):      
        matrizCuadriculada = []
        for fila in range(6):
            matrizCuadriculada.append([])
            for columna in range(10):
                if fila== 5 and columna == 0: 
                    matrizCuadriculada[fila].append(Base(self.framePG, self.ruta, False, True)) 
                elif fila== 5 and columna == 9:
                    matrizCuadriculada[fila].append(Base(self.framePG, self.ruta, False, False)) 
                elif (fila== 4 and columna == 9) or (fila== 5 and columna == 8): 
                    matrizCuadriculada[fila].append(SpawningPoint(self.framePG, self.ruta, 1))
                else:
                    matrizCuadriculada[fila].append(Casilla(self.framePG, self.ruta))  #Casilla() vacía
        return matrizCuadriculada
        

    def dibujarTablero(self):
        for fila in range( len(self.matriz)):
            for columna in range (len(self.matriz[fila])):
                objeto= self.matriz[fila][columna]
                objeto.dibujarCasilla(fila, columna)
        pygame.display.update()

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
        #self.matriz[fila][columna] = 1 #Cambiarle el color a la casilla
        print("Posición ", posicion, "Coordenadas en nuestra cuadrícula: ", fila, columna)
        return fila, columna

        ###Personajeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    def mover(self, x, y):
        terminar= False
        elemActual = self.matriz[x][y]
        self.matriz[x][y] = Casilla(self.framePG, self.ruta)

        while not terminar:
            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONUP:
                    nuevasCoord= self.getCasillaSeleccionada()
                    self.matriz[nuevasCoord[0]][nuevasCoord[1]] = elemActual
                    terminar = True
    def manejarEventos(self):
        while not self.terminar:
            self.dibujarTablero()
            self.btnCurar.dibujarBoton()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.salir()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    coordenadas = self.getCasillaSeleccionada()
                    if self.btnCurar.verificarPresionado():
                        
                    try:
                        self.mover(coordenadas[0], coordenadas[1])
                    except IndexError:
                        pass
            pygame.display.update()

class Arbitro():
    def __init__(self,listaJugadores):
        self.listaJugadores = listaJugadores
        self.enTurno = listaJugadores[0]#asignar el turno al primer jugador
        self.contadorTurnos = 0
        self.ubicacionEnlista = 0
    def getJugador1(self):
        return self.jugador1
    def getJugador2(self):
        return self.jugador2
    def getJugador3(self):
        return self.jugador3
    def sumarTurno(self):
        self.contadorTurnos+=1
    def asignarTurno(self):
        if self.ubicacionEnlista == 2:
            self.ubicacionEnlista = 0
        else:
            self.ubicacionEnlista += 1
        self.enTurno = listaJugadores[ubicacionEnlista]
    def restarAcciones(self):
        self.enTurno.sumarTurnos(-1)
        
            

class Vestibulo(pygame.sprite.Sprite):
    def __init__(self, titulo, dimensiones):
        pygame.sprite.Sprite.__init__(self) #herencia  
        #self.colorFondo = colorFondo
        self.framePG =  pygame.display.set_mode(dimensiones)
        self.ruta = os.path.dirname(__file__)#importante!! captura la ruta de este archivo sin importar la computadora
        self.imagen = pygame.image.load(os.path.join(self.ruta, "imagenes/bgVestibulo.jpg"))
        self.fondo = pygame.transform.scale(self.imagen, (dimensiones[0], dimensiones[1]))
        self.alien1 = Alien("Andrómeda",self.ruta,"imagenes/alien1.png")
        self.alien2 = Alien("Osa Mayor",self.ruta,"imagenes/alien2.png")
        self.alien3 = Alien("Orión",self.ruta,"imagenes/alien3.png")
        self.elegidos = []
        self.posX  =100
        self.posY = 290
        self.rojo = (220, 0, 0)
        self.verde = (0, 220, 0)
        self.gris = (155, 155, 155)
        pygame.display.set_caption(titulo)
        self.terminar = False
        self.btnsAndromeda = self.crearBotonesAndromeda()
        self.btnsOrion = self.crearBotonesOrion()
        self.btnsOsaMayor = self.crearBotonesOsaMayor()
        self.mantenerEscucha()

    """
    def crearBotones(self):
        botones = [];
        x = 100
        x_aux = x;
        contador = 0;
        for i in range(3):
            botones.append([])
            if i != 0:
                x += 320;  
                x_aux = x;
            for j in range(3):
                if contador==j and contador==i: 
                    color = self.rojo
                    contador+=1;
                else: 
                    color = self.verde
                botones[i].append(Boton(x_aux, 200,40,50, str(j+1), color, self.framePG))
                x_aux += 40;
        return botones;       
    """
    
    def crearBotonesAndromeda(self):
        botones = []
        botones.append(Boton(100, 200,40,50, "1", self.gris, self.framePG))
        botones.append(Boton(140, 200,40,50, "2", self.gris, self.framePG))
        botones.append(Boton(180, 200,40,50, "3", self.gris, self.framePG))
        return botones

    def crearBotonesOsaMayor(self):
        botones = []
        botones.append(Boton(420, 200,40,50, "1", self.gris, self.framePG))
        botones.append(Boton(460, 200,40,50, "2", self.gris, self.framePG))
        botones.append(Boton(500, 200,40,50, "3", self.gris, self.framePG))
        return botones

    def crearBotonesOrion(self):
        botones = []
        botones.append(Boton(740, 200,40,50, "1", self.gris, self.framePG))
        botones.append(Boton(780, 200,40,50, "2", self.gris, self.framePG))
        botones.append(Boton(820, 200,40,50, "3", self.gris, self.framePG))
        return botones

    def insertarImgs(self):
        self.framePG.blit(self.fondo, [0, 0])
        self.framePG.blit(self.alien1.getImagen(), (self.posX, self.posY))
        self.framePG.blit(self.alien2.getImagen(), (self.posX+280, 300))
        self.framePG.blit(self.alien3.getImagen(), (self.posX+600, 260))

    def jugar(self):
        self.terminar = True
        campoBatalla= CampoBatalla("Galaxia Zombi", 100, (1300, 600), (24, 22, 67), (88, 40, 165));
       
    def salir(self):
        pygame.quit()
        sys.exit()
        self.terminar = True

    def getPersonajeSeleccionado(self, listaBotones):
        numElegido = ""
        posicion = pygame.mouse.get_pos()#captura el lugar donde se da click
        for i in range(len(listaBotones)):
            if listaBotones[i].verificarPresionado(posicion):
                if listaBotones[i].getTxt() not in self.elegidos:
                    listaBotones[i].cambiarColorBtn(self.verde)
                    self.elegidos.append(listaBotones[i].getTxt())
        return numElegido
                    
    def getSeleccionados(self):
        botones = [self.btnsAndromeda, self.btnsOsaMayor, self.btnsOrion]
        for i in range(len(botones)):
            self.getPersonajeSeleccionado(botones[i])
        return print(self.elegidos)

    def mostrarHabilidades(self,palien):
        texto = palien.obtenerHabilidades()
##        fuente = pygame.font.Font(None,30)
##        mensaje = fuente.render(texto, 0, (200, 60, 80))
##        self.framePG.blit(mensaje, (0, 0))
        print(texto)
        
    def dibujarBotones(self):
        matrizBotones= [self.btnsAndromeda, self.btnsOsaMayor, self.btnsOrion]
        for i in range(len(matrizBotones)):
            for j in range(len(matrizBotones[i])):
                matrizBotones[i][j].dibujarBoton()
        
    def mantenerEscucha(self):#keep listening, esperando eventos
        while not self.terminar:
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    self.salir()
                elif eventos.type == pygame.KEYDOWN:
                    self.jugar()#metodo de jugar
                elif eventos.type == pygame.MOUSEBUTTONDOWN:
                    self.getSeleccionados()
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
        self.dimensiones = dimensiones
        self.imgZombie = pygame.image.load(os.path.join(self.ruta, "imagenes/titulo.png"))
        self.imgGalaxy = pygame.image.load(os.path.join(self.ruta, "imagenes/titulo2.png"))
        self.imagen = pygame.image.load(os.path.join(self.ruta, "imagenes/bgInicio.jpg"))
        self.fondo = pygame.transform.scale(self.imagen, (self.dimensiones[0], self.dimensiones[1]))
        self.posX  =100
        self.posY = 50
        self.framePG =  pygame.display.set_mode(dimensiones)
        pygame.display.set_caption(titulo)
        self.color = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))
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
        self.framePG.blit(self.fondo, [0, 0])
        self.framePG.blit(self.imgZombie, (self.posX, self.posY))
        self.framePG.blit(self.imgGalaxy, (self.posX+200, self.posY+100))

    def jugar(self):
        self.terminar = True
        Vestibulo("Personaje", (1012, 600))
        
    def salir(self):
        self.terminar = True
        pygame.quit()
        sys.exit()
        
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
        
