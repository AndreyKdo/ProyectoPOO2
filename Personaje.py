from random import random

class Personaje():
    vida=15
    ataque=2
    ubicacionX=0#indica la coordenada x
    ubicacionY=0#indica la coordena y
    def __init__(self,listaHabilidades):
        self.habilidades = listaHabilidades#lista de objetos tipo Habilidad
    def setUbicacion(self,x,y):
        self.x = x
        self.y = y
    def getUbicacion(self):
        return ubicacionX,ubicacionY
    def sumarVida(self,item):
        self.vida += item #item.getValor()#Sería así ya que recibe un objeto tipo Item
    def getVida(self):
        return self.vida
    def restarVida(self,ataqueRecibo):
        self.vida -= ataqueRecibo
    def getAtaque(self):
        return self.ataque
    def setAtaque(self,item):
        self.ataque += item #item.getValor()#Sería así ya que recibe un objeto tipo Item
    def atacar(self):
        pass #por hacer
    def morir(self):
        if self.vida <= 0:
            return True
        else:
            return False
    def mover(self,x,y):
        pass #por hacer
    def pasarTurno(self):
        pass #por hacer
    def usarHabilidad(self,habilidad):
        pass#en herencia
class Zombi(Personaje):
    veAlien=False
    escuchaRuido=False
    def __init__(self,item,habilidad):
        super().__init__(habilidad)
        self.item = item
    def soltarItem(self):
        if (self.vida <= 0) and random() < 0.5:#https://www.iteramos.com/pregunta/24686/obtener-un-valor-booleano-al-azar-en-python
            return self.item
        else:
            return False
    def setRuido(self):
        self.escuchaRuido = True
    def setVeAlien(self):
        self.veAlien = True
class Alien(Personaje):
    visible=False
    vulnerable=False
    inventario=[object]#lista de items
    def __init__(self,pnombre,habilidades):
        self.nombre=pnombre
        super().__init__(habilidades)
    def getInventario(self):
        return self.inventario
    def usarItem(self,item):
        pass#por hacer

