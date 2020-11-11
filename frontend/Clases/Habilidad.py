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
#para Alien Andrómeda
class MenosRuido(Habilidad):#solo funciona para alien, anula el ruido
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.setRuido(self.valor)
#para Alien Andrómeda
class Teletransporte(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)  
    def usarHabilidad(self,personaje,destino):
        personaje.setUbicacion(destino)
#para Alien Andrómeda
class Confusion(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.restarVida(self.valor)
#para Alien Osa Mayor
class Escalar(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje,casilla):
        personaje.setUbicacion(casilla)
#para Alien Osa Mayor
class MultiAtaque(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        for i in range(1,self.valor):
            personaje.atacar()
#para Alien Osa Mayor
class TurnoExtra(Habilidad):#solo funciona para alien
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.sumarTurnos(self.valor)
#para Alien Orión
class MasAlcance(Habilidad):#solo funciona para alien
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.sumarRango(self.valor)
#para Alien Orión
class RepeleAtaque(Habilidad):#funciona tanto para aliens como para zombis
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.setVulnerable(False)
#para Alien Orión
class Invisible(Habilidad):#solo funciona para alien
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,personaje):
        personaje.setVisible(False)

"""
Habilidades únicas para zombis
"""
class OidoAgudo(Habilidad):#se mueve más casillas si escucha ruido
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,zombi):
        zombi.setRuido(10)
class Rapidez(Habilidad):
    def __init__(self, nombre, valor, descripcion):
        super().__init__(nombre, valor, descripcion)
    def usarHabilidad(self,zombi):
        for i in range(self.valor):
            zombi.mover()
