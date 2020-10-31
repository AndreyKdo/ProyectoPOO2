class Item():
    def __init__(self,categoria,nombre):
        self.categoria = categoria
        self.nombre = nombre
    def getCategoria(self):
        return categoria
    def getNombre(self):
        return nombre
    def setCategoria(self,categoria):
        self.categoria = categoria
    def setNombre(self,nombre):
        self.nombre = nombre

class Pocima(Item):
    def __init__(self, nombre):
        super().__init__("pocima", nombre)
    def curar(self,personaje):
        i =  personaje.getVida() - personaje.getVidaMax()
        personaje.restarVida(i)
class Potenciador(Item):
    def __init__(self, nombre,experiencia):
        super().__init__("potenciador", nombre)
        self.experiencia = experiencia
    def aplicarExp(self):
        return self.experiencia
class Arma(Item):
    def __init__(self, nombre, ruido, alcance):
        super().__init__("arma", nombre)
        self.nivelRuido = ruido
        self.alcance = alcance
    def hacerRuido(self):
        return self.nivelRuido
    def getAlcance(self):
        return self.alcance