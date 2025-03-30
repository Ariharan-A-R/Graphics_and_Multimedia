import pygame as pg
from OpenGL.GL import *
import numpy as np
class App:
    def __init__(self):
        pg.init()  # Initialize pygame modules
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)  # Fix here
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.2, 1)
        self.mainLoop()

    def mainLoop(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:  # Fix: Use uppercase QUIT
                    running = False
            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def quit(self):
        pg.quit()

class Triangle:
    def __init__(self):
        self.vertices=(
            -0.5,-0.5,0.0,1.0,0.0,0.0,
            0.5,-0.5,0.0,0.0,1.0,0.0,
            0.0,0.5,0.0,0.0,0.0,1.0
        )
        self.vertices=np.array(self.vertices,dtype=np.float32)
        self.vertex_count=3
        self.vao=glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vao=glGenBuffers(1)
        

if __name__ == "__main__":
    myApp = App()
