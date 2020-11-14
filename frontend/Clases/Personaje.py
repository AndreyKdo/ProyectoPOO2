import pygame;
import os, sys;
from random import random
from Clases.Habilidad import *
from Clases.Item import *
"""
Clase Padre Personaje
"""
class Personaje():
    vidaMaxima=10
    vida=vidaMaxima-3
    ataque=2
    rangoAtaque = 1
    rangoMovimiento = 1
    vulnerable=True#False
    ubicacionAnterior = ()
    ubicacion = ()
    #enTurno = False #para verificar que esté en turno
    def __init__(self,listaHabilidades,acciones):
        self.accionesTurno = acciones
        self.habilidades = listaHabilidades#lista de objetos tipo Habilidad
    def getUbicacionAnterior(self):
        return self.ubicacionAnterior
    def getUbicacion(self):
        return self.ubicacion
    def setUbicacion(self,x,y):
        self.ubicacionAnterior = self.ubicacion
        self.ubicacion = (x,y)
    def getVidaMax(self):
        return vidaMaxima
    def avanzarNivel(self,item):
        exp = item.aplicarExp()
        if self.vida < self.vidaMaxima:
            self.vida += exp - (self.vidaMaxima-self.vida)
        self.vidaMaxima += exp
        self.ataque += exp
        self.vida = self.vidaMaxima
    def getVidaMaxima(self):
        return self.vidaMaxima
    def getVidaActual(self):
        return self.vida
    def restarVida(self,ataqueRecibo):
        if self.vulnerable:
            self.vida -= ataqueRecibo
    def getAtaque(self):
        return self.ataque
    def setAtaque(self,valor):
        self.ataque += valor
    def getVulnerable(self):
        return self.vulnerable
    def getHabilidades(self):
        return self.habilidades
    def setVulnerable(self,booleano):
        self.vulnerable = booleano
    def sumarTurnos(self,turnos):
        self.accionesTurno += turnos
    def atacar(self):
        self.accionesTurno -= 1
    def morir(self):
        if self.vida <= 0:
            return True
        else:
            return False
    def getRangoAtaque(self):
        return self.rangoAtaque
    def getRangoMovimiento(self):
        return self.rangoMovimiento
    """def pasarTurno(self):
        self.enTurno = False
    def setEnTurno(self):
        if self.enTurno:
            self.enTurno = False
        else:
            self.enTurno = True
    def getEnTurno(self):
        return self.enTurno"""
    def sumarRango(self,sumador):
        self.rangoAtaque+=sumador
"""
Subclase Zombi
"""
class Zombi(Personaje):
    veAlien=False
    escuchaRuido=False
    def __init__(self,item,habilidad):
        super().__init__(habilidad,1)#listaHabilidades, acciones por turno, baseZombi(es un objeto tipo Casilla)
        self.item = item
    def soltarItem(self):
        if (self.morir()) and random() < 0.5:#https://www.iteramos.com/pregunta/24686/obtener-un-valor-booleano-al-azar-en-python
            return self.item
        else:
            return False
    def setRuido(self,nivelRuido):
        if nivelRuido > 5:
            self.escuchaRuido = True
        else:
            self.escuchaRuido = False        
    def setVeAlien(self,ve):
        self.veAlien = ve
"""
Subclase Alien
"""
class Alien(Personaje):
    def __init__(self,pnombre,ruta,imagen):#,habilidades
        self.nombre=pnombre
        self.visible=False
        #listas de ítems
        self.pocimas = [Pocima("Frasco de Sol"),Pocima("Leche de Vía Láctea")]
        self.potenciadores = [Potenciador("Cuerno de Taurus",2)]
        #argumentos de armas: nombre,ruido,alcance
        self.armas = [Arma("Golpe Alien", 1, 1)]
        self.armaEquipada=self.armas[0]#atributo tipo Arma
        self.nivelRuido=0
        self.imgAlien = pygame.image.load(os.path.join(ruta, imagen))
        super().__init__(self.definirHabilidades(),3) #listaHabilidades, acciones por turno y baseAlien(es un objeto tipo Casilla)
    def setImagen(self,ruta,imagen,objetoPY=True):
        #objetoPY es para indicar que se trata de una imagen tipo objeto de pygame
        #si recibe false al atributo se le asigna solo el string de la ubicacion de la imagen
        if objetoPY:
            self.imgAlien = pygame.image.load(os.path.join(ruta, imagen))
        else:
            self.imgAlien = imagen
    def getNombre(self):
        return self.nombre
    #obtiene las habilidades en un texto
    def obtenerHabilidades(self):
        texto = "Habilidades de "+self.getNombre()+":"
        for habilidad in self.getHabilidades():
            texto += "\n*       "+habilidad.nombre+":       "+habilidad.descripcion+"\n"
        return texto  
    def definirHabilidades(self):
        listaHabilidades = []
        if self.nombre == "Andrómeda":
            #anula el sonido de una casilla
            listaHabilidades.append(MenosRuido("Silenciantenas (Silencio):",10,"Los silenciosos habitantes de esta galaxia son imperceptibles al oído humano... al menos la mayoría del tiempo."))
            listaHabilidades.append(Teletransporte("Cinturón de Gusano (Teletransporte):",2,"Este simpático alienígena tiene la afición de visitar los lugares que anteriormente ha visitado,\n tanto así que se ha fabricado un cinturón a partir de espacio-tiempo."))
            listaHabilidades.append(Confusion("Mirada Confusa (Confusión):",5,"¡No mires a este alienígena directamente a los ojos! \n   La última vez que un humano lo hizo, este comenzó a morderse la lengua y a pegarse el dedo chiquito del pie."))
            self.armas.append(Arma("Meteoritov", 10, 10))
        elif self.nombre == "Osa Mayor":
            listaHabilidades.append(Escalar("Tentáculosos (Escalar): ",1,"Los habitantes de esta constelación no necesitan ascensor, ni escaleras, ni arnés.\n ¿Escalar el Himalaya? Eso es como dar un paseo en el parque."))
            listaHabilidades.append(MultiAtaque("Octo-Punch (Multi-Ataque):",2,"Para este alienígena aparentemente pacífico, las artes marciales es como aprender a caminar.\n Mejor ve consiguiendo cita con el dentista... y unos 4 cascos de fibra de carbono."))
            listaHabilidades.append(TurnoExtra("Fast-Opus (Turno Extra): ",5,"La capacidad de realizar múltiples tareas al mismo tiempo es algo con lo que soñamos.\n Osa Mayor es una gran ayuda para mis proyectos de programación."))
            self.armas.append(Arma("Rayo Láser", 5, 5))
        else: #Si self.nombre == "Orión":
            listaHabilidades.append(MasAlcance("Cazador (Más Alcance):",1,"Los habitantes de Orión son grandes cazadores que atinan cualquier dardo desde grandes distancias.\n Dales cualquier tipo de arma, ponte una manzana en la cabeza y trata de cerrar los ojos antes de su tiro."))
            listaHabilidades.append(RepeleAtaque("Elastipiel (Repele-Ataque):",2,"Este alienígena es profesional en esquivar hasta el más mínimo embate.\n ¡Orión es una constelación genial para jugar quemados!"))
            listaHabilidades.append(Invisible("Traje de Invisibilidad: ",5,"Sus ropas lo hacen ser imperceptible a todo ojo del universo conocido.\n ¡Quiero su traje para espiar a mi gato en la noche sin que me vea!"))
        return listaHabilidades
    def restarAcciones(self):
        self.accionesTurno-=1
    def getAccionesDisponibles(self):
        if self.accionesTurno==0:
            self.accionesTurno = 3
            return 0
        else:
            return self.accionesTurno
    def atacar(self):
        alcance,ruido = self.armaEquipada.usar()
        self.nivelRuido+=ruido
        self.ataque+=alcance
    def usarPocima(self,indice):
        self.pocimas[indice].usar(self)
        self.pocimas.pop(indice)
    def usarPotenciador(self,indice):
        self.subirNivel(self.potenciadores[indice].usar())
        self.potenciadores.pop(indice)
    def usarArma(self,indice):
        self.rangoAtaque -= self.armaEquipada.getAlcance()
        self.nivelRuido -= self.armaEquipada.getRuido()
        self.armaEquipada = self.armas[indice]
        self.rangoAtaque += self.armaEquipada.getAlcance()
    """def setVisible(self,booleano):
        self.visible = booleano
    def getRuido(self):
        return self.nivelRuido
    def setRuido(self,reductor):
        self.nivelRuido -= reductor
    def setRuido(self,ruidoGenerado):
        self.nivelRuido = ruidoGenerado"""
    def getImagen(self):
        return self.imgAlien
    def subirNivel(self,experiencia):
        self.vidaMaxima += experiencia
        self.ataque += experiencia // 2
    """Métodos relacionados con los items"""
    #agregar nuevos items
    def agregarPocimas(self,pocima):
        self.pocimas.append(pocima)
    def agregarPotenciadores(self,potenciador):
        self.potenciadores.append(potenciador)
    def agregarArmas(self,arma):
        self.armas.append(arma)
    #obtener listas de items
    def getPocimas(self):
        return self.pocimas
    def getPotenciadores(self):
        return self.potenciadores
    def getArmas(self):
        return self.armas
    def getArmaEquipada(self):
        return self.armaEquipada
    #verificar que tiene items
    def tienePocimas(self):
        if self.pocimas!=[]:
            return True
        else:
            return False
    def tienePotenciadores(self):
        if self.potenciadores!=[]:
            return True
        else:
            return False
    def tieneArmas(self):
        if len(self.armas)>1:
            return True
        else:
            return False
