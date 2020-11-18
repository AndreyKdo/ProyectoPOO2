import os, sys;
import time
import random
import pygame
from Clases.Casilla import *
from Clases.Personaje import Alien
from Clases.Personaje import Zombi


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
    def setColor(self,color):
        self.color = color
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

class PC():
    def __init__(self):
        self.ruta= os.path.dirname(__file__)
        self.apolo= Zombi("Apolo", self.ruta, "imagenes/miniApolo.png")
        self.troyano= Zombi("Troyano", self.ruta, "imagenes/miniTroyano.png")
        self.centauro = Zombi("Centauro", self.ruta, "imagenes/miniCentauro.png")
        self.jugadores = []
    
    def crearZombiRandom(self):
        posiblesZombis = [self.apolo, self.troyano, self.centauro]
        zombi = random.choice(posiblesZombis)
        return zombi

    def agregarZombi(self):
        zombi = self.crearZombiRandom()
        self.jugadores.append(zombi)
        return zombi
        print("se agregó zombi random")

    def jugarTurno(self):
        print("se llegó a la PC")
        #self.agregarZombi()

    def getJugadores(self):
        return self.jugadores
    
    def getJugadorReciente(self):
        return self.jugadores[-1];


class Arbitro():
    def __init__(self,listaJugadores):
        self.ruta = os.path.dirname(__file__)
        self.listaJugadores = listaJugadores
        self.rival = PC()
        self.enTurno = listaJugadores[0]#asigna el turno al primer jugador autom.
        self.contadorTurnos = 0
        self.ubicacionEnlista = 0
        self.asignarImgMinis()
        self.asignarUbicacionInicial()
        self.turnoRival = False
    def getTurnoRival(self):
        return self.turnoRival
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

    def getRivalReciente(self):
        return self.rival.getJugadorReciente()

    def sumarTurno(self):
        self.contadorTurnos+=1

    def setUbicacionLista(self):
        if self.ubicacionEnlista == 2:#·len(self.listaJugadores)-1:
            self.ubicacionEnlista = 0
            self.contadorTurnos+=1
            self.turnoRival = True
        else:
            self.ubicacionEnlista += 1
            self.turnoRival = False
    def evaluarFin(self):
        for alien in self.listaJugadores:
            if alien.morir()==False:
                return False
        return True
    def asignarTurno(self):
        #turnoZombi = False    
        if self.ubicacionEnlista == 2:#len(self.listaJugadores)-1:
            self.ubicacionEnlista = 0
            self.contadorTurnos+=1
            self.turnoRival = True
        else:
            self.turnoRival = False
            self.ubicacionEnlista += 1
        self.enTurno = self.listaJugadores[self.ubicacionEnlista]   
        #return turnoZombi

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
        self.maxX = 2
        self.minY = 7
        self.ruta = os.path.dirname(__file__)
        self.framePG = self.dibujarCampoBatalla()
        self.listaSpwnPts = self.instanciarSpwnPts()
        self.matriz = self.generarMatriz()
        
        self.fuente = pygame.font.Font(None, 30)
        self.fuente1 = pygame.font.SysFont("Gadugi", 17)
        self.fuente2 = pygame.font.SysFont("Chiller", 35)
        #self.casilla = Casilla(self.framePG, self.matriz, "", self.dimCuadros)
        self.terminar =False
        self.miniJugador1 = pygame.image.load(os.path.join(self.ruta, Arbitro.getJugador1().getImagen()))
        self.miniJugador2 = pygame.image.load(os.path.join(self.ruta, Arbitro.getJugador2().getImagen()))
        self.miniJugador3 = pygame.image.load(os.path.join(self.ruta, Arbitro.getJugador3().getImagen()))
        self.btnCurar = Boton(1080, 200,150,50, "Curar","btncurar",(155, 155, 155), self.framePG)
        self.btnPotenciar = Boton(1080, 340,150,50, "Potenciar","btnpotenciar",(155, 155, 155), self.framePG)
        
        self.pasarPocima = 0
        self.pasarPotenciador = 0
        self.pasarArma = 0
        self.manejarEventos()

    def dibujarBotones(self):
        self.btnCurar.dibujarBoton()
        self.btnPotenciar.dibujarBoton()
        #boton curar
        if self.Arbitro.getJugadorEnTurno().tienePocimas():
            self.btnCurar.setColor((36,222,11))
            self.mostrarPocimaDisponible()
            #print("Pocimas:",self.Arbitro.getJugadorEnTurno().getPocimas()[0].getNombre())
        else:
            self.btnCurar.setColor((155, 155, 155))
        #boton potenciar
        if self.Arbitro.getJugadorEnTurno().tienePotenciadores():
            self.btnPotenciar.setColor((36,222,11))
            self.mostrarPotenciadorDisponible()
            #print("Potenciadores",self.Arbitro.getJugadorEnTurno().getPotenciadores()[0].getNombre())
        else:
            self.btnPotenciar.setColor((155, 155, 155))

        #print("Armas:",self.Arbitro.getJugadorEnTurno().getArmas()[0].getNombre())
        #print("Arma Equipada:",self.Arbitro.getJugadorEnTurno().getArmaEquipada().getNombre())

    def asignarBloque(self, x, y):
        if 0<=x<=2:
            if 0<=y<=4:
                return 1
            else: #entre 5 y 9
                return 2
        else: #entre 3 y 5
            if 0<=y<=4:
                return 3
            else: #entre 5 y 9
                return 4

    def definirPrioridad(self, bloque, x):
        if bloque==1 or bloque==2:
            return ["abajo", "izquierda", "derecha", "arriba"]
        elif bloque==4:
            return ["izquierda", "abajo", "arriba", "derecha"]
        else:
            if x==3 or x==4:
                return ["abajo", "izquierda", "derecha", "arriba"]
            elif x==5:
                return ["izquierda", "abajo", "arriba", "derecha"] 


    def aparecerZombi(self, x, y, listaPrioridades, spwnPt, zombi):
        ubicado = False
        #print("apareciendo un zombi, x y y originales", x, y)
        #print(listaPrioridades)
        #print("tipo de zombie ", zombi.getNombre())
        for i in range(len(listaPrioridades)):
            if not ubicado:
                direccion = self.evaluarPrioridad(listaPrioridades[i], spwnPt)
                if direccion != False:          
                    #print("direccion sugerida", direccion)
                    if direccion == "izquierda":
                        #print("entró izq")
                        y -= 1
                    elif direccion == "derecha":
                        #print("entró der")
                        y += 1
                    elif direccion == "arriba":
                        #print("entró arriba")
                        x -= 1
                    else: #abajo
                        #print("entró al else: se asume que abajo")
                        x += 1
                    #print("apareciendo a un zombi, x y y nuevos: ", x, y)
                    if self.matriz[x][y].getTipo() == "estandar" or self.matriz[x][y].getTipo() == "casillaAlien": #si la casilla esta vacia o había un alien (se lo come)
                        self.matriz[x][y].setTipo("casillaZombi")
                        self.matriz[x][y].setImagen(zombi.getImagen()) 
                        self.matriz[x][y].setPersonaje(zombi)
                        ubicado= True
                    #else: #había ya un zombi, u otro sp
                        #continue
                
             #peor de los casos: no logró ubicar al zombi, (ningun SP tiene todos los lados cerrados)
            
    def activarSpwnPts(self):
        contador = 0
        for fila in range(len(self.matriz)):
            for columna in range(len(self.matriz[fila])):
                if self.matriz[fila][columna].getTipo() == "sp": 
                    bloque= self.asignarBloque(fila, columna)
                    listaPrioridades = self.definirPrioridad(bloque, fila)
                    zombi = self.Arbitro.rival.agregarZombi()
                    self.aparecerZombi(fila, columna, listaPrioridades, self.matriz[fila][columna], zombi)
                    contador +=1
        #print("se activaron", contador, "spwn pts existentes")

    def instanciarSpwnPts(self):
        sp = SpawningPoint(self.framePG, self.ruta, False, False, False, False)
        spA = SpawningPoint(self.framePG, self.ruta, True, False, False, False)
        spB = SpawningPoint(self.framePG, self.ruta, False, True, False, False)
        spC = SpawningPoint(self.framePG, self.ruta, False, False, True, False)
        spD = SpawningPoint(self.framePG, self.ruta, False, False, False, True)
        spAB = SpawningPoint(self.framePG, self.ruta, True, True, False, False)
        spBC = SpawningPoint(self.framePG, self.ruta, False, True, True, False) 
        spCD = SpawningPoint(self.framePG, self.ruta, False, False, True, True) 
        spABC = SpawningPoint(self.framePG, self.ruta, True, True, True, False)
        spBCD = SpawningPoint(self.framePG, self.ruta, False, True, True, True)
        spPts= [sp, spA, spB, spC, spD, spAB, spBC, spCD, spABC, spBCD]
        return spPts        

    def evaluarPrioridad(self, indice, SpawningPoint):
        if indice == "derecha" and not SpawningPoint.getBloqueoDer():
            direccion = "derecha"
        elif indice == "izquierda" and not SpawningPoint.getBloqueoIzq():
            direccion = "izquierda"
        elif indice == "arriba" and not SpawningPoint.getBloqueoArriba():
            direccion = "arriba"
        elif indice == "abajo" and not SpawningPoint.getBloqueoAbajo():
            direccion = "abajo"
        else:
            return False
        return direccion

    def evaluarPosicion(self, x, y):
        if 0<=x<=5 and 0<=y<=9:
            if self.matriz[x][y].getTipo() == "casillaAlien": #si porque se lo come :P 
                return True
            elif self.matriz[x][y].getTipo() == "estandar": #si porque está vacía
                return True
            else:
                print("cumple los índices pero no es ni casilla alien ni estandar")
                return False
        else:
            print("no cumplió los indice en evaluar posición")
            return False
    
    def matarZombi(self, x, y):
        pass
    # sacar de desplazar

    def desplazarZombi(self, x, y):
        pass

    def seguirRuido(self, ataque, x, y):
        #F R = no  he seteado que escuchen el ruido en ningún lado 
        #Nuevas coordenadas
        #verificar los zombies que puedan escuharlo
        for fila in range(len(self.matriz)):
            for columna in range(len(self.matriz[fila])):
                if self.matriz[fila][columna].getTipo() == "casillaZombi":
                    if self.matriz[fila][columna].getTipo().escuchaRuido():
                        try:
                            if x < fila: #el ruido esta arriba
                                if self.verificarCasilla(fila -1, columna, "estandar"):
                                    self.desplazarZombi(fila -1, columna)
                                elif self.verificarCasilla(fila -1, columna, "casillaZombi"):
                                    self.matarZombi(fila -1, columna)

                            elif x > fila: #si el ruido esta abajo
                                if self.verificarCasilla(fila +1, columna, "estandar"):
                                    self.desplazarZombi(fila +1, columna)
                                elif self.verificarCasilla(fila +1, columna, "casillaZombi"):
                                    self.matarZombi(fila +1, columna)

                            elif y < columna:#ruido a la izq
                                if self.verificarCasilla(fila, columna-1, "estandar"):
                                    self.desplazarZombi(fila, columna-1)
                                elif self.verificarCasilla(fila, columna-1, "casillaZombi"):
                                    self.matarZombi(fila, columna-1)
                            else:
                                if self.verificarCasilla(fila, columna +1, "estandar"):
                                    self.desplazarZombi(fila, columna +1)
                                elif self.verificarCasilla(fila, columna +1, "casillaZombi"):
                                    self.matarZombi(fila, columna +1)
                        except:
                            pass
                            #print("algo anda mal, posiblemente se sale de los índices existentes")

    def generarSpwnPt(self):
        contador = 0
        x = random.randint(1, self.maxX)
        y = random.randint(self.minY, 8)

        if self.matriz[x][y].getTipo() == "estandar":
            spwnPt = random.choice(self.listaSpwnPts) #se cambia la casilla vacía por una con SpwnPt random de la lista
            self.matriz[x][y] = spwnPt
            if self.maxX<4:
                self.maxX += 1
                #print("nuevo maxX: ", self.maxX)
            if 1<self.minY:
                self.minY -=1 
                #print("nuevo minY: ", self.minY)

            bloque= self.asignarBloque(x, y)
            listaPrioridades = self.definirPrioridad(bloque, x)
            zombi= self.Arbitro.rival.agregarZombi() #Rival reciente es la ultima pos de la lista de zombies que genera la PC
            self.aparecerZombi(x, y, listaPrioridades, spwnPt, zombi)
            contador +=1 
            #print(" generó un sp, hay ", contador)
        else: 
            pass
            #print("no generó sp, hay ", contador, "casilla a la que quiso acceder ", x, y)

    def desplazarZombis(self):
        permitido = False
        
        for fila in range(len(self.matriz)):
            x = fila
            for columna in range(len(self.matriz[fila])):
                y = columna
                if self.matriz[fila][columna].getTipo() == "casillaZombi":
                    bloque= self.asignarBloque(fila, columna)
                    #print("bloque: ",bloque)
                    listaPrioridades = self.definirPrioridad(bloque, fila)   
                    #print(listaPrioridades)
                    for i in range(len(listaPrioridades)):
                        #print("Corrida del for #", i+1, "dirección de la lista que se esta evaluando ", listaPrioridades[i])
                        if not permitido:
                            if listaPrioridades[i] == "izquierda":
                                #print("desplazamiento izquierda")
                                y = columna -1
                                permitido = self.evaluarPosicion(x, y)

                            elif listaPrioridades[i] == "derecha":
                                #print("desplazamiento derecha")
                                y = columna +1
                                permitido = self.evaluarPosicion(x, y)

                            elif listaPrioridades[i] == "arriba":
                                #print("desplazamiento arriba")
                                x = fila -1
                                permitido = self.evaluarPosicion(x, y)
                            elif listaPrioridades[i] == "abajo":
                                #print("desplazamiento abajo")
                                x = fila +1
                                permitido = self.evaluarPosicion(x, y)
                            else:
                                #print("el else del desplazamiento, posiblemente el zombi quedó encerrado")
                                pass
                        
                    if permitido and self.matriz[x][y].getTipo() == "casillaAlien":
                        #print("entró a setear el desplazamiento")
                        print("*********Personaje comido:",self.matriz[x][y].getPersonaje().getNombre())
                        self.matriz[x][y].getPersonaje().restarVida(10)

                        self.matriz[fila][columna].setTipo("estandar")
                        self.matriz[x][y].setTipo("casillaZombi")

                        personaje = self.matriz[fila][columna].getPersonaje() #moviendo el zombi
                        self.matriz[x][y].setPersonaje(personaje)

                        imagen = self.matriz[fila][columna].getImagen()
                        self.matriz[x][y].setImagen(imagen)
                        
                        self.matriz[fila][columna] = Casilla(self.framePG, self.ruta) #ojoooo, veamos si le guarda todo lo que tenia seteado
                        print("se lo comeee")
                        ###PENSAAAR QUE HACER CON EL TURNO DEL ALIEN
                    elif permitido and self.matriz[x][y].getTipo() == "estandar":                
                        #print("solo avanza")
                        #print("casilla anterior:", fila, columna, "ahora hay", self.matriz[fila][columna].getPersonaje() )
                        #print("casilla nueva:", x, y, "ahora hay", self.matriz[x][y].getPersonaje())
                        self.matriz[fila][columna].setTipo("estandar")
                        self.matriz[x][y].setTipo("casillaZombi")

                        personaje = self.matriz[fila][columna].getPersonaje() #ojoooo, veamos si le guarda todo lo que tenia seteado
                        self.matriz[x][y].setPersonaje(personaje)

                        imagen = self.matriz[fila][columna].getImagen()
                        self.matriz[x][y].setImagen(imagen)
                        
                        self.matriz[fila][columna] = Casilla(self.framePG, self.ruta)
                    else:
                        pass
                        #print("no permitido, y/o no tipo alien o casilla")
              
    def generarMatriz(self):      
        matrizCuadriculada = []
        for fila in range(6):
            matrizCuadriculada.append([])
            for columna in range(10):
                if fila== 5 and columna == 0: 
                    matrizCuadriculada[fila].append(Base(self.framePG, self.ruta, False, True)) 
                elif fila== 0 and columna == 9:
                    matrizCuadriculada[fila].append(Base(self.framePG, self.ruta, False, False)) 
                #elif (fila== 4 and columna == 9) or (fila== 5 and columna == 8): 
                    #matrizCuadriculada[fila].append(SpawningPoint(self.framePG, self.ruta, 1))
                else:
                    matrizCuadriculada[fila].append(Casilla(self.framePG, self.ruta))  #Casilla() vacía
                    if fila== 4 and columna == 1:
                        matrizCuadriculada[fila][columna].setTipo("casillaAlien")
                        matrizCuadriculada[fila][columna].setImagen(self.Arbitro.getJugador1().getImagen())
                        matrizCuadriculada[fila][columna].setPersonaje(self.Arbitro.getJugador1())
                    elif fila== 4 and columna == 0:
                        matrizCuadriculada[fila][columna].setTipo("casillaAlien")
                        matrizCuadriculada[fila][columna].setImagen(self.Arbitro.getJugador2().getImagen())
                        matrizCuadriculada[fila][columna].setPersonaje(self.Arbitro.getJugador2())
                    elif fila== 5 and columna == 1:
                        matrizCuadriculada[fila][columna].setTipo("casillaAlien")
                        matrizCuadriculada[fila][columna].setImagen(self.Arbitro.getJugador3().getImagen())
                        matrizCuadriculada[fila][columna].setPersonaje(self.Arbitro.getJugador3())
                    elif (fila==1 and columna==9):
                        matrizCuadriculada[fila][columna].setTipo("casillaZombi")
                        zombi = self.Arbitro.rival.agregarZombi()
                        matrizCuadriculada[fila][columna].setImagen(zombi.getImagen())
                        matrizCuadriculada[fila][columna].setPersonaje(zombi)
                        #Turno Pc debería tener un método para insertar un zombi random después de los trunos de los aliens
                    else:
                        matrizCuadriculada[fila][columna].setTipo("estandar")
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
    ###Personajeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    def getCasillaSeleccionada(self):
        posicion = pygame.mouse.get_pos()#devuelve la posicion de la ventana donde se dio click 
        columna = posicion[0] // ( self.dimCuadros + 1) #width
        fila = posicion[1] // ( self.dimCuadros + 1) #altura
        return fila, columna

    def verificarCasilla(self,x,y,tipoVerificar):
        if self.matriz[x][y].getTipo() == tipoVerificar:
            return True
        else:
            return False
    def verificarCercania(self,x,y,rangoMovimiento="mover"):
        if rangoMovimiento == "mover":
            rangoMovimiento = self.Arbitro.getJugadorEnTurno().getRangoMovimiento()
        ubicacion = self.Arbitro.getJugadorEnTurno().getUbicacion()        
        if (x == ubicacion[0]-rangoMovimiento or x == ubicacion[0]+rangoMovimiento or x == ubicacion[0]) and (y == ubicacion[1]-rangoMovimiento or y == ubicacion[1] or y == ubicacion[1]+rangoMovimiento):
            return True 
        else:
            return False 
    def mover(self, x, y):        
        if self.verificarCasilla(x,y,"estandar") and self.verificarCercania(x,y):
            #guarda en una variable auxiliar la casilla con el personaje a mover
            campoAuxiliar = self.matriz[self.Arbitro.getJugadorEnTurno().getUbicacion()[0]][self.Arbitro.getJugadorEnTurno().getUbicacion()[1]]
            #asigna a la ubicación del jugador una casilla estándar
            self.matriz[self.Arbitro.getJugadorEnTurno().getUbicacion()[0]][self.Arbitro.getJugadorEnTurno().getUbicacion()[1]] = Casilla(self.framePG, self.ruta)
            self.matriz[self.Arbitro.getJugadorEnTurno().getUbicacion()[0]][self.Arbitro.getJugadorEnTurno().getUbicacion()[1]].setTipo("estandar")
            #asigna al campo seleccionado el auxiliar que almacena al personaje
            self.matriz[x][y] = campoAuxiliar
            self.Arbitro.getJugadorEnTurno().setUbicacion(x,y)#cambia la ubicación logicamente    
            return True
        else:
            return False
    def verificarAtacar(self,x,y):
        ubicacion = self.Arbitro.getJugadorEnTurno().getUbicacion()
        rangoAtaque = self.Arbitro.getJugadorEnTurno().getRangoAtaque()
        if self.verificarCercania(x,y,rangoAtaque) and self.verificarCasilla(x,y,"casillaZombi"):
            return True
        else:
            return False
    def atacar(self,x,y):
        if self.verificarAtacar(x,y):
            self.matriz[x][y].getPersonaje().restarVida(self.Arbitro.getJugadorEnTurno().getAtaque())
            self.Arbitro.getJugadorEnTurno().restarAcciones()#resta una acción del turno
            return True
        else:
            return False
    def actualizarAcciones(self):
        imagen = pygame.image.load(os.path.join(self.ruta, self.Arbitro.getJugadorEnTurno().getImagen()))
        pygame.draw.rect(self.framePG, self.colorLineas, [1016, 19, 400, 800], 0)#rectangulo de dibujo
        textoJugador = self.fuente.render("Turno del Jugador:" +str(self.Arbitro.getTurno()),True, (255, 255, 255))
        self.framePG.blit(imagen, (1130, 88))
        textoVida = self.fuente.render("Vida Disponible:"+str(self.Arbitro.getJugadorEnTurno().getVidaActual())+"/"+str(self.Arbitro.getJugadorEnTurno().getVidaMaxima()),True, (255, 255, 255))
        self.framePG.blit(textoJugador, (1016, 50))
        self.framePG.blit(textoVida, (1016, 19))
        self.dibujarBotones()
        self.mostrarArmas()
    #métodos para curar el Alien en turno
    def mostrarPocimaDisponible(self):
        textoAyuda = "Presiona 'a' para más pócimas."
        if self.pasarPocima > len(self.Arbitro.getJugadorEnTurno().getPocimas())-1:
            textoAyuda = "Ya no hay más pócimas."
            self.pasarPocima = 0
        texto = self.fuente1.render("Pócima: " +self.Arbitro.getJugadorEnTurno().getPocimas()[self.pasarPocima].getNombre(),True, (255, 255, 255))
        texto2 = self.fuente1.render(textoAyuda,True, (255, 255, 255))
        self.framePG.blit(texto, (1015, 262))
        self.framePG.blit(texto2, (1015, 290))
    def llamarCurar(self):
        if self.btnCurar.getColor()==(36,222,11):#verifica que el boton de curar esté en verde
            #después verifica que la vida del personaje se pueda curar
            if self.Arbitro.getJugadorEnTurno().getVidaActual()<self.Arbitro.getJugadorEnTurno().getVidaMaxima():
                self.Arbitro.getJugadorEnTurno().usarPocima(self.pasarPocima)
                self.Arbitro.getJugadorEnTurno().restarAcciones()#resta una acción del turno
                return True
        return False
    #métodos para potenciar el Alien en turno
    def mostrarPotenciadorDisponible(self):
        textoAyuda = "Presiona 's' para más potenciadores."
        if self.pasarPotenciador > len(self.Arbitro.getJugadorEnTurno().getPotenciadores())-1:
            textoAyuda = "Ya no hay más potenciadores."
            self.pasarPotenciador = 0
        texto = self.fuente1.render("Potenciador: " +self.Arbitro.getJugadorEnTurno().getPotenciadores()[self.pasarPotenciador].getNombre(),True, (255, 255, 255))
        texto2 = self.fuente1.render(textoAyuda,True, (255, 255, 255))
        self.framePG.blit(texto, (1015, 390))
        self.framePG.blit(texto2, (1015, 425))
    def llamarPotenciar(self):
        if self.btnPotenciar.getColor()==(36,222,11):#verifica que el boton de potenciar esté en verde
            self.Arbitro.getJugadorEnTurno().usarPotenciador(self.pasarPotenciador)
            self.Arbitro.getJugadorEnTurno().restarAcciones()#resta una acción del turno
            return True
        else:
            return False
    def mostrarArmas(self):
        textoAyuda = "Presiona 'd' para cambiar arma."
        if self.pasarArma > len(self.Arbitro.getJugadorEnTurno().getArmas())-1:
            textoAyuda = "No hay más armas."
            self.pasarArma = 0
        self.Arbitro.getJugadorEnTurno().usarArma(self.pasarArma)
        texto1 = self.fuente1.render("Arma Equipada: ",True, (255, 255, 255))
        texto2 = self.fuente2.render(self.Arbitro.getJugadorEnTurno().getArmaEquipada().getNombre(),True, (255, 255, 255))
        texto3 = self.fuente1.render(textoAyuda,True, (255, 255, 255))
        pygame.draw.rect(self.framePG, (27,27,55), [1014, 470, 280, 200], 0)#rectangulo de dibujo
        imagen = pygame.image.load(os.path.join(self.ruta, self.Arbitro.getJugadorEnTurno().getArmaEquipada().getImagen()))
        self.framePG.blit(imagen, (1200, 510))
        self.framePG.blit(texto1, (1100, 477))
        self.framePG.blit(texto2, (1050, 510))
        self.framePG.blit(texto3, (1021, 570))
    def manejarEventos(self):   
        ataque = False   
        while not self.terminar:             
            if self.Arbitro.evaluarFin():
                pygame.draw.rect(self.framePG, (180,66,16), [10, 19, 1000, 900], 0)#rectangulo de dibujo
                finJuego = self.fuente.render("Fin del Juego... Presione ESC para salir." ,True, (0,0,0))
                self.framePG.blit(finJuego, (10, 19))
            else:
                self.dibujarTablero()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.salir()
                    elif evento.key == pygame.K_a:
                        self.pasarPocima += 1
                    elif evento.key == pygame.K_s:
                        self.pasarPotenciador += 1
                    elif evento.key == pygame.K_d:
                        #Depende del arma escogida .setAtaque(), puños <4, laser <7, meteoro<10 
                        self.pasarArma += 1
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.Arbitro.getJugadorEnTurno().morir()==False:
                        if self.btnCurar.verificarPresionado(pygame.mouse.get_pos()):
                            self.llamarCurar()
                        elif self.btnPotenciar.verificarPresionado(pygame.mouse.get_pos()):
                            self.llamarPotenciar()  
                        try:
                            coordenadas = self.getCasillaSeleccionada()                       
                            if self.mover(coordenadas[0], coordenadas[1]):
                                self.Arbitro.getJugadorEnTurno().restarAcciones()#resta una acción del turno
                            elif self.atacar(coordenadas[0], coordenadas[1]):
                                #saber el ataque que se hizo para setear el atributo ataque de Personaje
                                self.Arbitro.getJugadorEnTurno().restarAcciones()#resta una acción del turno                                               
                                # zombi cercano . restarVida(ataque)
                        except IndexError:
                            pass #Error: debe seleccionar una ubicación de la matriz mostrada
            if self.Arbitro.getJugadorEnTurno().getAccionesDisponibles()==0:
                self.Arbitro.asignarTurno()
                if self.Arbitro.getTurnoRival():
                    if ataque != False and ataque > 3:
                        self.seguirRuido(ataque)
                    else: 
                        self.desplazarZombis()
                    #self.activarSpwnPts()
                    self.generarSpwnPt()       
            self.actualizarAcciones()
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
        self.fuente1 = pygame.font.SysFont("Bookman Old Style", 17)
        self.fuente2 = pygame.font.SysFont("Castellar", 25)
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
        campoBatalla= CampoBatalla("¡Que comience la batalla!", 100, (1300, 600), (24, 22, 67), (88, 40, 165),Arbitro(self.personajes))
               
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
        #for i in range(len(self.personajes)
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
        print(texto)
        
    def dibujarBotones(self):
        matrizBotones= [self.btnsAndromeda, self.btnsOsaMayor, self.btnsOrion]
        for i in range(len(matrizBotones)):
            for j in range(len(matrizBotones[i])):
                matrizBotones[i][j].dibujarBoton()
    def imprimirDescripcion(self,palien):
        listaDescripcion = palien.obtenerHabilidades().split("\n")
        #print(listaDescripcion)
        x,y=10, 13
        for linea in listaDescripcion:
            if y == 13:
                descripcion = self.fuente2.render(linea,True, (255, 255, 255))
                self.framePG.blit(descripcion, (290, y))
                y+=20
            else:
                plinea = linea.split(":")
                for oracion in plinea:                        
                    descripcion = self.fuente1.render(oracion,True, (255, 255, 255))
                    self.framePG.blit(descripcion, (x, y))
                    y+=16
    def fondoTemporal(self,imagen):
        imagenTemp = pygame.image.load(os.path.join(self.ruta, imagen))            
        self.framePG.blit(pygame.transform.scale(imagenTemp, (1012, 600)), [0, 0])
        #rectangulo transparente obtenido de https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        s = pygame.Surface((995, 270))  # the size of your rect
        s.set_alpha(128)                # alpha level
        s.fill((0,0,0)) 
        self.framePG.blit(s, (0,0))

    def mostrarDescripcion(self):
        #Se lee por la posición del mouse mediante el método pygame.mouse.get_pos()       
        if pygame.mouse.get_pos()[0]>=110 and pygame.mouse.get_pos()[0]<=190 and pygame.mouse.get_pos()[1]>=325 and pygame.mouse.get_pos()[1]<=500:#"Ubicación de Andrómeda"
            pygame.draw.rect(self.framePG, (18,204,230), [10, 13, 995, 250], 0)#rectangulo de dibujo
            self.fondoTemporal("imagenes/andromedaGalaxy.jpg")
            self.framePG.blit(self.andromeda.getImagen(), (self.posX, self.posY))
            self.imprimirDescripcion(self.andromeda)
        elif pygame.mouse.get_pos()[0]>=430 and pygame.mouse.get_pos()[0]<=525 and pygame.mouse.get_pos()[1]>=315 and pygame.mouse.get_pos()[1]<=520:#"Ubicación de Osa Mayor"            
            self.fondoTemporal("imagenes/osaMayorConstelacion.jpg")
            self.framePG.blit(self.osaMayor.getImagen(), (self.posX+280, 300))
            self.imprimirDescripcion(self.osaMayor)
        elif pygame.mouse.get_pos()[0]>=750 and pygame.mouse.get_pos()[0]<=840 and pygame.mouse.get_pos()[1]>=317 and pygame.mouse.get_pos()[1]<=440:#"Ubicación de Orión"
            pygame.draw.rect(self.framePG, (18,204,230), [10, 13, 995, 250], 0)#rectangulo de dibujo
            self.fondoTemporal("imagenes/orionConstelacion.jpg")
            self.framePG.blit(self.orion.getImagen(), (self.posX+600, 260))
            self.imprimirDescripcion(self.orion)
        else: pass

    def mantenerEscucha(self):#keep listening, esperando eventos
        while not self.terminar:
            
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    self.salir()
                elif eventos.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                    self.getSeleccionados() 
                else:
                    pass 
            #framePG.blit(self.imgTitulo,(100,100))
            self.insertarImgs()
            self.dibujarBotones()
            self.mostrarDescripcion()
            
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
        Vestibulo("Elige el orden de tus personajes, ¡Arrastra el mouse sobre ellos para hacerlo sabiamente!", (1012, 600))
        
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
    Inicio("Zombie Galaxy: una batalla entre Aliens y Zombis", (1012, 600));
        
