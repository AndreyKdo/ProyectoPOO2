import pygame;
import os, sys;
from random import random
from Clases.Habilidad import *

"""
Clase Padre Personaje
"""
class Personaje():
    vidaMaxima=10
    vida=vidaMaxima
    ataque=2
    rangoAtaque = 1
    vulnerable=False
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
    """def mover(self):#valida hacia donde mover, puede ser distinto en zombi y en alien
        self.accionesTurno -= 1"""
    def getVidaMax(self):
        return vidaMaxima
    def avanzarNivel(self,item):
        exp = item.aplicarExp()
        if self.vida < self.vidaMaxima:
            self.vida += exp - (self.vidaMaxima-self.vida)
        self.vidaMaxima += exp
        self.ataque += exp
    def getVidaMaxima(self):
        return self.vidaMaxima
    def getVidaActual(self):
        return self.vida
    def restarVida(self,ataqueRecibo):
        if vulnerable:
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
    visible=False
    inventario=[object]#lista de items
    armaEquipada="Arma"#atributo tipo Arma
    nivelRuido=1
    nombre = ""
    def __init__(self,pnombre,ruta,imagen):#,habilidades
        self.nombre=pnombre
        self.imgAlien = pygame.image.load(os.path.join(ruta, imagen))
        super().__init__(self.definirHabilidades(),3) #listaHabilidades, acciones por turno y baseAlien(es un objeto tipo Casilla)
    def setImagen(self,ruta,imagen,objetoPY=True):
        #objetoPY es para indicar que se trata de una imagen tipo objeto de pygame
        #si recibe false al atributo se asigna solo el string de la imagen
        if objetoPY:
            self.imgAlien = pygame.image.load(os.path.join(ruta, imagen))
        else:
            self.imgAlien = imagen
    def getNombre(self):
        return self.nombre
    def obtenerHabilidades(self):
        texto = "Habilidades de "+self.getNombre()+":\n"
        for habilidad in self.getHabilidades():
            texto += "\n"+habilidad.nombre+":"+habilidad.descripcion+"\n"
        return texto
    def definirHabilidades(self):
        listaHabilidades = []
        if self.nombre == "Andrómeda":
            #anula el sonido de una casilla
            listaHabilidades.append(MenosRuido("Silenciantenas",10," Los silenciosos habitantes de esta galaxia son imperceptibles al oído humano... al menos la mayoría del tiempo."))
            listaHabilidades.append(Teletransporte("Cinturón de Gusano",2," Este simpático alienígena tiene la afición de visitar los lugares que anteriormente ha visitado, tanto así que se ha fabricado un cinturón a partir de espacio-tiempo."))
            listaHabilidades.append(Confusion("Mirada Confusa",5," ¡No mires a este alienígena directamente a los ojos! La última vez que un humano lo hizo, este comenzó a morderse la lengua y a pegarse el dedo chiquito del pie."))
        elif self.nombre == "Osa Mayor":
            listaHabilidades.append(Escalar("Tentáculosos",1," Los habitantes de esta constelación no necesitan ascensor, ni escaleras, ni arnés. ¿Escalar el Himalaya? Eso es como dar un paseo en el parque para este espécimen."))
            listaHabilidades.append(MultiAtaque("Octo-Punch",2," Para este alienígena aparentemente pacífico, las artes marciales es como aprender a caminar. Si te enfrentas con él, mejor ve consiguiendo cita con el dentista... y unos 4 cascos de fibra de carbono."))
            listaHabilidades.append(TurnoExtra("Fast-Opus",5," Una vez pusieron a competir a este Alienígena con el actual Récord Guiness de armar cubos de rubik. El reloj no había ni comenzado a marcar el segundo, cuando este fue batido ¡8 veces! Obtiene un turno extra con su capacidad."))
        else: #Si self.nombre == "Orión":
            listaHabilidades.append(MasAlcance("Cazador",1," Los habitantes de Orión son por naturaleza grandes cazadores que atinan la jabalina a un punto específico desde grandes distancias. Dales cualquier tipo de arma, ponte una manzana en la cabeza y trata de cerrar los ojos antes de su tiro."))
            listaHabilidades.append(RepeleAtaque("Elastipiel",2," Este alienígena es profesional en esquivar hasta el más mínimo embate. ¡Orión es una constelación genial para jugar quemados!"))
            listaHabilidades.append(Invisible("Traje de Invisibilidad",5," Él puede pasar frente tus narices sin que lo veas, sus ropas lo hacen ser imperceptible a todo ojo del universo conocido. ¡Quiero su traje para espiar a mi gato en la noche sin que me vea!"))
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
        self.nivelRuido+=armaEquipada.hacerRuido()
        return super().atacar()
    def usarItem(self,item):
        pass#por hacer
    def getInventario(self):
        return self.inventario
    def getArma(self):
        return self.armaEquipada
    def setVisible(self,booleano):
        self.visible = booleano
    def getRuido(self):
        return self.nivelRuido
    def setRuido(self,reductor):
        self.nivelRuido -= reductor
    """def setRuido(self,ruidoGenerado):
        self.nivelRuido = ruidoGenerado"""
    def getImagen(self):
        return self.imgAlien


