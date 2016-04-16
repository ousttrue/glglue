# coding: utf-8

from OpenGL.GLUT import *
import sys
import simple_renderer

'''
01からglutに関連する部分だけを抜き出した。
OpenGLに関連する部分は無くなった。
'''

def reshape_func(w, h):
    simple_renderer.resize(w, h == 0 and 1 or h)

def disp_func():
    simple_renderer.draw()
    glutSwapBuffers()

if __name__=="__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(256, 256)
    glutCreateWindow(sys.argv[0].encode('ascii'))
    glutDisplayFunc(disp_func)
    glutIdleFunc(disp_func)
    glutReshapeFunc(reshape_func)

    simple_renderer.initialize()

    glutMainLoop()

