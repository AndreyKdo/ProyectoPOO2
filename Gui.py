import pygame;
import os;
import tkinter as tk;

class CampoBatalla():
    def __init__(self, titulo, dimCuadros, dimFrame, colorCuadros, colorLineas):
        self.titulo = titulo;
        self.dimCuadros = dimCuadros; #100
        self.dimFrame = dimFrame; #(1012, 600);
        self.colorCuadros = colorCuadros; #azul = (24, 22, 67);
        self.colorLineas = colorLineas; #morado = (88, 40, 165);

    def dibujarCampo(self):
        pygame.init()
        framePG = pygame.display.set_mode(self.dimFrame)
        pygame.display.set_caption(self.titulo)
        clock = pygame.time.Clock()
        terminar = False
        while not terminar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminar = True
            framePG.fill(self.colorLineas)
            for i in range(1, self.dimFrame[0], self.dimCuadros + 1):
                for j in range(1, self.dimFrame[1], self.dimCuadros + 1):
                    pygame.draw.rect(framePG, self.colorCuadros, [i, j, self.dimCuadros, self.dimCuadros], 0)
            pygame.display.flip()
            clock.tick(1)
        pygame.quit()

class Ventana():
    # Por parámetro le pasamos el componente raíz al constructor root= Tk() = master
    def __init__(self, dimensiones, titulo):
        # Dimensiones de la ventana 
        self.root = tk.Tk()
        self.root.geometry(dimensiones) #1200 x 600
        self.root.title(titulo)
   
class Escenario(Ventana):
    def __init__(self, framePG, dimensiones, titulo, colorFondo):
        super().__init__(dimensiones, titulo)  
        self.colorFondo = colorFondo
        contenedorPG = tk.Frame(self.root, width = 500, height = 500) #mismos que el frameog
        contenedorPG.pack()

        frame = tk.Frame(self.root, width = 75, height = 500)
        frame.pack()
        os.environ['SDL_WINDOWID'] = str(contenedorPG.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        framePG.fill(pygame.Color(24, 22, 67))

        pygame.display.init()
        pygame.display.update()


class Menu(Ventana):
    def __init__(self, dimensiones, titulo, colorFondo):
        super().__init__(dimensiones, titulo)  
        #self.colorFondo = colorFondo
         
        # Botones
        btnJugar = tk.Button(self.root, text="Jugar", command=self.jugar)
        btnJugar.pack()

        btnSalir = tk.Button(self.root, text="Salir", command=self.salir)
        btnSalir.pack()

        self.root.mainloop();

    # Definimos la función como un método de clase
    def jugar(self):
        self.root.destroy();
        azul= (24, 22, 67)
        morado= (88, 40, 165)
        campoBatalla= CampoBatalla("Aliens Vs. Zombies", 100, (1012, 600), azul, morado);
        framePG= campoBatalla.dibujarCampo()
        

    def salir(self):
        self.root.destroy();


# Instanciamos la clase
if __name__ == "__main__":
    app = Menu("1200x600", "Menú", (88, 40, 165))
