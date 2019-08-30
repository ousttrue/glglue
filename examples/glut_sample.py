# coding: utf-8
'''
# glut
require pyOpenGL + glut.dll
require pyOpenGL + freeglut.dll

# glut install on Windows

* glut.dllもしくはfreeglut.dllを入手(vcpkgでビルドするのおすすめ)
* Python.exeと同じフォルダにコピーするか環境変数PATHを設定する
'''

import pathlib
import sys
HERE = pathlib.Path(__file__).absolute().parent
sys.path.insert(0, str(HERE.parent / 'src'))

if __name__ == "__main__":
    import glglue.gl3
    import glglue.glut
    controller = glglue.gl3.SampleController()
    glglue.glut.mainloop(controller)
