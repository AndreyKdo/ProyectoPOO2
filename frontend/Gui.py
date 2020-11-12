import os, sys;
import random
import pygame
from Clases.Casilla import *
from Clases.Personaje import Alien


class Boton():   
    def __init__(self,x,y,ancho,alto,texto, identificador,  color, screen):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.textoBoton = texto
        self.id = identificador
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
    
    def getID(self):
        return self.id
    def getColor(self):
        return self.color
    def cambiarColorBtn(self, nuevoColor):
        self.color = nuevoColor
        
class Arbitro():
    def __init__(self,listaJugadores):
        self.ruta = os.path.dirname(__file__)
        self.listaJugadores = listaJugadores
        self.enTurno = listaJugadores[0]#asigna el turno al primer jugador autom.
        self.contadorTurnos = 0
        self.ubicacionEnlista = 0
        self.asignarImgMinis()
        self.asignarUbicacionInicial()
    def asignarImgMinis(self):
        for jugador in self.listaJugadores:
            if jugador.getNombre() == "Andrómeda":
                jugador.setImagen(self.ruta,"imagenes/miniAndromeda.png",False)#envía false para indicar que no es un tipo objeto de pygame
            elif jugador.getNombre() == "Osa Mayor":
                jugador.setImagen(self.ruta,"imagenes/miniOsaMayor.png",False)
            else:
                jugador.setImagen(self.ruta,"imagenes/miniOrion.png",False)
        
    def asignarUbicacionInicial(self):
        self.listaJugadores[0].setUbicacion(4,1)
        #print("ubicaciòn jugador 1:",self.listaJugadores[0].getUbicacion())
        self.listaJugadores[1].setUbicacion(4,0)
        #print("ubicaciòn jugador 2:",self.listaJugadores[1].getUbicacion())
        self.listaJugadores[2].setUbicacion(5,1)
        #print("ubicaciòn jugador 3:",self.listaJugadores[2].getUbicacion())
        
    def getJugador1(self):
        return self.listaJugadores[0]
    def getJugador2(self):
        return self.listaJugadores[1]
    def getJugador3(self):
        return self.listaJugadores[2]
    def sumarTurno(self):
        self.contadorTurnos+=1
    def asignarTurno(self):
        print("Jugador turno Anterior:",self.enTurno.getNombre())
        if self.ubicacionEnlista == 2:
            self.ubicacionEnlista = 0
        else:
            self.ubicacionEnlista += 1
        self.enTurno = self.listaJugadores[self.ubicacionEnlista]
        print("Jugador turno Actual:",self.enTurno.getNombre())
    def restarAcciones(self):
        self.enTurno.sumarTurnos(-1)
    def getJugadorEnTurno(self):
        return self.enTurno
    def getTurno(self):
        return self.ubicacionEnlista+1
    
class CampoBatalla(pygame.sprite.Sprite):
    def __init__(self, titulo, dimCuadros, dimFrame, colorCuadros, colorLineas,Arbitro):
        pygame.sprite.Sprite.__init__(self) #herencia
        self.Arbitro = Arbitro#atributo del arbitro del juego
        self.titulo = titulo
        self.dimCuadros = int(dimCuadros) #100
        self.dimFrame = dimFrame; #(1012, 600);
        self.colorCuadros = colorCuadros; #azul = (24, 22, 67);
        self.colorLineas = colorLineas; #morado = (88, 40, 165)
        self.ruta = os.path.dirname(__file__)
        self.framePG = self.dibujarCampoBatalla()
        self.matriz = self.generarMatriz()
        self.btnCurar = Boton(1153, 46,40,50, "Curar","btncurar",(155, 155, 155), self.framePG)#self.crearBotones()
        self.fuente = pygame.font.Font(None, 30)
        #self.casilla = Casilla(self.framePG, self.matriz, "", self.dimCuadros)
        self.terminar =False
        self.manejarEventos()
        self.miniJugador1 = pygame.image.load(os.path.join(self.ruta, Arbitro.getJugador1().getImagen()))
        self.miniJugador2 = pygame.image.load(os.path.join(self.ruta, Arbitro.getJugador2().getImagen()))
        self.miniJugador3 = pygame.image.load(os.path.join(self.ruta, Arbitro.getJugador3().getImagen()))
      #self.Arbitro.asignarTurno()
    #def llamarCurar(self):
    #def setMiniAlien(self):
    #    self.miniAlien = self.Arbitro.getJugadorEnTurno().getImagen()
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
                    if fila== 4 and columna == 1:
                        matrizCuadriculada[fila][columna].setTipo("inicial")
                        matrizCuadriculada[fila][columna].setImagen(self.Arbitro.getJugador1().getImagen())
                    #elif fila==4 and columna == 0:
                    #    matrizCuadriculada[fila][columna].setImagen("imagenes/miniAndromeda.png")
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
        pygame.display.flip()
        #pygame.display.update() 
        return framePG
    """
    def insertarMinis(self):
        self.framePG.blit(self.miniJugador1, (Arbitro.getJugador1().getUbicacion()[0], Arbitro.getJugador1().getUbicacion()[1]))
        self.framePG.blit(self.miniJugador2, (Arbitro.getJugador2().getUbicacion()[0], Arbitro.getJugador2().getUbicacion()[1]))
        self.framePG.blit(self.miniJugador3, (Arbitro.getJugador3().getUbicacion()[0], Arbitro.getJugador3().getUbicacion()[1]))
    """    
    def getCasillaSeleccionada(self):
        posicion = pygame.mouse.get_pos()
        columna = posicion[0] // ( self.dimCuadros + 1) #width
        fila = posicion[1] // ( self.dimCuadros + 1) #altura
        #self.matriz[fila][columna] = 1 #Cambiarle el color a la casilla
        print("Posición ", posicion, "Coordenadas en nuestra cuadrícula: ", fila, columna)
        return fila, columna
    
        ###Personajeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    def mover(self, x, y):
        print("MOVER:",x,y)#casilla seleccionada
        terminar= False
        elemActual = self.matriz[x][y]
        self.matriz[x][y] = Casilla(self.framePG, self.ruta)

        while not terminar:
            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONUP:
                    nuevasCoord= self.getCasillaSeleccionada()
                    self.matriz[nuevasCoord[0]][nuevasCoord[1]] = elemActual
                    #self.Arbitro.getJugadorEnTurno().setUbicacion()
                    self.Arbitro.getJugadorEnTurno().restarAcciones()
                    terminar = True
                                      
    def actualizarTextos(self):
        textoVida = self.fuente.render("Vida Disponible:" + str(self.Arbitro.getJugadorEnTurno().getVidaMaxima())+"/"+str(self.Arbitro.getJugadorEnTurno().getVidaActual()),True, (255, 255, 255))
        pygame.draw.rect(self.framePG, (255, 0, 0), [1016, 19, 400, 800], 0)#self.colorLineas
        #pygame.draw.rect(self.framePG, (255, 0, 0), [1016, 19, 400, 400], 0)
        textoJugador = self.fuente.render("Turno del Jugador:" +str(self.Arbitro.getTurno()),True, (255, 255, 255))
        self.framePG.blit(textoVida, (1016, 19))
        self.framePG.blit(textoJugador, (1016, 50))
        #self.matriz[4][1].
    def manejarEventos(self):
        #frameActualiza = pygame.display.set_mode()
        
        while not self.terminar:  
            #self.setMiniAlien()
            #self.framePG.blit(self.miniAlien,(1016, 19))
            self.dibujarTablero()
            #self.btnCurar.dibujarBoton()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.salir()
                elif evento.type == pygame.MOUSEBUTTONDOWN:                    
                    #self.framePG.fill()
                    #if self.btnCurar.verificarPresionado(pygame.mouse.get_pos()):
                    #   print("curar")
                    try:
                        coordenadas = self.getCasillaSeleccionada()
                        self.mover(coordenadas[0], coordenadas[1])                        
                    except IndexError:
                        pass
            if self.Arbitro.getJugadorEnTurno().getAccionesDisponibles()==0:
                self.Arbitro.asignarTurno()
            self.actualizarTextos()
            pygame.display.update()      
            

class Vestibulo(pygame.sprite.Sprite):
    def __init__(self, titulo, dimensiones):
        pygame.sprite.Sprite.__init__(self) #herencia  
        #self.colorFondo = colorFondo
        self.framePG =  pygame.display.set_mode(dimensiones)
        self.ruta = os.path.dirname(__file__)#importante!! captura la ruta de este archivo sin importar la computadora
        self.imagen = pygame.image.load(os.path.join(self.ruta, "imagenes/bgVestibulo.jpg"))
        self.fondo = pygame.transform.scale(self.imagen, (dimensiones[0], dimensiones[1]))
        self.andromeda = Alien("Andrómeda",self.ruta,"imagenes/andromeda.png")
        self.osaMayor = Alien("Osa Mayor",self.ruta,"imagenes/osaMayor.png")
        self.orion = Alien("Orión",self.ruta,"imagenes/orion.png")
        self.personajes= []
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
    
    def crearBotonesAndromeda(self):
        botones = []
        botones.append(Boton(100, 200,40,50, "1", "andromeda", self.gris, self.framePG))
        botones.append(Boton(140, 200,40,50, "2", "andromeda", self.gris, self.framePG))
        botones.append(Boton(180, 200,40,50, "3", "andromeda", self.gris, self.framePG))
        return botones

    def crearBotonesOsaMayor(self):
        botones = []
        botones.append(Boton(420, 200,40,50, "1", "osaMayor", self.gris, self.framePG))
        botones.append(Boton(460, 200,40,50, "2", "osaMayor", self.gris, self.framePG))
        botones.append(Boton(500, 200,40,50, "3", "osaMayor", self.gris, self.framePG))
        return botones

    def crearBotonesOrion(self):
        botones = []
        botones.append(Boton(740, 200,40,50, "1", "orion", self.gris, self.framePG))
        botones.append(Boton(780, 200,40,50, "2", "orion", self.gris, self.framePG))
        botones.append(Boton(820, 200,40,50, "3", "orion", self.gris, self.framePG))
        return botones

    def insertarImgs(self):
        self.framePG.blit(self.fondo, [0, 0])
        self.framePG.blit(self.andromeda.getImagen(), (self.posX, self.posY))
        self.framePG.blit(self.osaMayor.getImagen(), (self.posX+280, 300))
        self.framePG.blit(self.orion.getImagen(), (self.posX+600, 260))

    def jugar(self):
        self.terminar = True
        campoBatalla= CampoBatalla("Galaxia Zombi", 100, (1300, 600), (24, 22, 67), (88, 40, 165),Arbitro(self.personajes))
        
        
    def salir(self):
        pygame.quit()
        sys.exit()
        self.terminar = True

    def instanciarAliens(self):
        self.elegidos.sort()
        for i in range(len(self.elegidos)):
            if self.elegidos[i][1] == "andromeda":
                self.personajes.append(self.andromeda)
            elif self.elegidos[i][1] == "osaMayor":
                self.personajes.append(self.osaMayor)
            else: #Si self.nombre == "orion":
                self.personajes.append(self.orion)
        self.jugar()
        #Impresión de prueba
        #for i in range(len(self.personajes)):
         #  print(self.personajes[i].getNombre())

    def getPersonajeSeleccionado(self, listaBotones):
        for i in range(len(listaBotones)):
            if listaBotones[i].verificarPresionado(pygame.mouse.get_pos()):
                if len(self.elegidos)>0:
                    for j in range(len(self.elegidos)):#valida que el jugador según el número no tenga seleccionado un personaje
                        if int(listaBotones[i].getTxt()) in self.elegidos[j]:
                            return
                listaBotones[i].cambiarColorBtn(self.verde)
                self.elegidos.append((int(listaBotones[i].getTxt()), listaBotones[i].getID()))
                    
    def getSeleccionados(self):
        botones = [self.btnsAndromeda, self.btnsOsaMayor, self.btnsOrion]
        for i in range(len(botones)):
            self.getPersonajeSeleccionado(botones[i])
        if len(self.elegidos) == 3:
            self.instanciarAliens()

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
                    self.jugar()
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
        
