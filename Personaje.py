from random import random

class Personaje():
    vida=15
    ataque=2
    rangoAtaque = 1
    vulnerable=False
    def __init__(self,listaHabilidades,acciones,casilla):
        self.ubicacion = casilla #es un tipo de objeto casilla
        self.accionesTurno = acciones
        self.habilidades = listaHabilidades#lista de objetos tipo Habilidad
    def getUbicacion(self):
        return self.ubicacion
    def setUbicacion(self,casilla):
        self.ubicacion = casilla
    def mover(self):#valida hacia donde mover, puede ser distinto en zombi y en alien
        self.accionesTurno -= 1
    def getVida(self):
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
    def setVulnerable(self,booleano):
        self.vulnerable = booleano
    def sumarTurnos(self,turnos):
        self.accionesTurno += turnos
    def atacar(self):
        self.accionesTurno -= 1
        pass #por hacer
    def morir(self):
        if self.vida <= 0:
            return True
        else:
            return False
    def pasarTurno(self):
        pass #por hacer
    def sumarRango(self,sumador):
        self.rangoAtaque+=sumador
"""
Subclase Zombi
"""
class Zombi(Personaje):
    veAlien=False
    escuchaRuido=False
    def __init__(self,item,habilidad):
        super().__init__(habilidad,1,"baseZombi")#listaHabilidades, acciones por turno, baseZombi(es un objeto tipo Casilla)
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
    def __init__(self,pnombre,habilidades):
        self.nombre=pnombre
        super().__init__(habilidades,3,"baseAlien") #listaHabilidades, acciones por turno y baseAlien(es un objeto tipo Casilla)
    def usarItem(self,item):
        self.accionesTurno -= 1
        pass#por hacer
    def getInventario(self):
        return self.inventario
    def getArma(self):
        return self.armaEquipada
    def setVisible(self,booleano):
        self.visible = booleano
    def getRuido(self):
        return self.nivelRuido
    def setRuido(self,ruidoGenerado):
        self.nivelRuido = ruidoGenerado


