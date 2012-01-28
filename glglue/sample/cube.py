# coding: utf-8
from OpenGL.GL import *


class Cube(object):
    def __init__(self, s):
        self.vertices=[
                -s, -s, -s,
                 s, -s, -s,
                 s,  s, -s,
                -s,  s, -s,
                -s, -s,  s,
                 s, -s,  s,
                 s,  s,  s,
                -s,  s,  s,
                ]
        self.colors=[
                0, 0, 0,
                1, 0, 0,
                0, 1, 0,
                0, 0, 1,
                0, 1, 1,
                1, 0, 1,
                1, 1, 1,
                1, 1, 0,
                ]
        self.indices=[
                0, 1, 2, 2, 3, 0,
                0, 4, 5, 5, 1, 0,
                1, 5, 6, 6, 2, 1,
                2, 6, 7, 7, 3, 2,
                3, 7, 4, 4, 0, 3,
                4, 7, 6, 6, 5, 4,
                ]

    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY);
        glVertexPointer(3, GL_FLOAT, 0, self.vertices);
        glEnableClientState(GL_COLOR_ARRAY);
        glColorPointer(3, GL_FLOAT, 0, self.colors);
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, self.indices);
        glDisableClientState(GL_COLOR_ARRAY);
        glDisableClientState(GL_VERTEX_ARRAY);

