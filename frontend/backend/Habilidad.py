class Habilidad():
    def __init__(self,nombre,valor,descripcion):
        self.nombre=nombre
        self.valor=valor
        self.descripcion=descripcion
    def usarHabilidad(self):
        pass

"""
Habilidades especiales para Aliens (la mayoría se puede generalizar para todo personaje)
"""
class MenosRuido(Habilidad):#solo funciona para alien
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.setRuido(self.valor)

class Teletransporte(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion,casilla):
        super().__init__(nombre, valor, descripcion)  
        self.destino = casilla
    def usarHabilidad(self,personaje):
        personaje.setUbicacion(self.destino)

class Confusion(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.restarVida(self.valor)
 
class Escalar(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion,casilla):
        super().__init__(nombre, valor, descripcion)
        self.obstaculo = casilla
    def usarHabilidad(self,personaje):
        personaje.setUbicacion(self.obstaculo)

class MultiAtaque(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        for i in range(1,self.valor):
            personaje.atacar()

class TurnoExtra(Habilidad):#solo funciona para alien
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.sumarTurnos(self.valor)

class masAlcance(Habilidad):#solo funciona para alien
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.sumarRango(self.valor)

class repeleAtaque(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.setVulnerable(False)

class invisible(Habilidad):#solo funciona para alien
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.setVisible(False)

"""
Habilidades únicas para zombis
"""
class oidoAgudo(Habilidad):
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,zombi):
        zombi.setRuido(10)
class rapidez(Habilidad):
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,zombi):
        for i in range(self.valor):
            zombi.mover()