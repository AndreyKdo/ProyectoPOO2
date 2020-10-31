class Casilla:
    def __init__(self, framePG, tipo):
        self.tipo = ""
        self.framePG = framePG
        # ---------------------
        #image_path = os.path.join("data", "images")
        #self.image = pygame.image.load(os.path.join(image_path, filename)).convert_alpha()
        #self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
   
class Obstaculo(Casilla):
    def __init__(self, tipo, bloqueoIzq, bloqueoDer, bloqueoArr, bloqueoAba):
        super().__init__(self, tipo)
        self.bloqueoIzq = bloqueoIzq
        self.bloqueoDer = bloqueoDer
        self.bloqueoArr = bloqueoArr
        self.bloqueoAba = bloqueoAba
        self.imgObst = 'obstaculo.png'

    def setBloqueoIzq(self, bloqueoIzq):
        self.bloqueoIzq #preguntar 

    def consultarBloqueoIzq(self, bloqueoIzq):
        return self.bloqueoIzq

class Base(Casilla):
    def __init__(self, tipo, conquistada, aliada):
        super().__init__(self, tipo)
        self.imgBaseAliada = 'baseZombie.png'
        self.imgBaseEnemiga = 'baseAlien.png'

    def evaluarConquistada(self):
        pass

class SpawningPoint(Casilla):
    def __init__(self, tipo, zombi):
        super().__init__(self, tipo)
        #self.zombi = Zombi()
        self.imgSpPt = 'spwnPt.png'
        #self.dimCuadros = 100 #OJO que está alambrado

    def crearZombi(self):
        pass