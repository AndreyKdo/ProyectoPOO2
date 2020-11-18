class Item():
    def __init__(self,categoria,nombre):
        self.categoria = categoria
        self.nombre = nombre
        self.imagen = self.definirImagen()
    def definirImagen(self):
        pass
    def getCategoria(self):
        return self.categoria
    def getNombre(self):
        return self.nombre
    def setCategoria(self,categoria):
        self.categoria = categoria
    def setNombre(self,nombre):
        self.nombre = nombre
    def usar(self):
        pass
class Pocima(Item):
    def __init__(self, nombre):
        super().__init__("pocima", nombre)
    def usar(self,personaje):
        i =  personaje.getVidaActual() - personaje.getVidaMaxima()
        personaje.restarVida(i)
class Potenciador(Item):
    def __init__(self, nombre,experiencia):
        super().__init__("potenciador", nombre)
        self.experiencia = experiencia
    def usar(self):
        return self.experiencia
class Arma(Item):
    def __init__(self, nombre, ruido, alcance):
        super().__init__("arma", nombre)
        self.nivelRuido = ruido
        self.alcance = alcance
        self.imagen = self.definirImagen()
    def definirImagen(self):
        if self.nombre=="Meteoritov":
            return "imagenes/meteoro.png"
        elif self.nombre=="Rayo Láser":
            return "imagenes/laser.png"
        else:
            return "imagenes/golpe.png"

    def getImagen(self):
        return self.imagen
    def getRuido(self):
        return self.nivelRuido
    def getAlcance(self):
        return self.alcance
    def usar(self):
        return self.getAlcance(),self.getRuido()