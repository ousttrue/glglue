# coding: utf-8
'''
# glut
requrie pyOpenGL + glut.dll

# glut install on Windows

* なんとかしてglut.dllを入手(vcpkgでビルドするのおすすめ)
* Python.exeと同じフォルダにコピーする。
'''

import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parents[1]))
import glglue.sample
import glglue.glut


if __name__ == "__main__":
    controller = glglue.sample.SampleController()
    glglue.glut.mainloop(controller)
