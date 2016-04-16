# coding: utf-8
'''
## glut
requrie pyOpenGL + glut install

###glut install on Windows

1. download glut-3.7.6-bin.zip from http://user.xmission.com/~nate/glut.html
2. copy glut32.dll to C:/PythonXX/
'''


import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parents[1]))
import glglue.sample
import glglue.glut


if __name__=="__main__":
    controller=glglue.sample.SampleController()
    glglue.glut.mainloop(controller)
