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
    import glglue.sample
    import glglue.glut
    controller = glglue.sample.SampleController()

    # manual loop
    lastclock = 0
    loop = glglue.glut.LoopManager(controller)
    while True:
        # require freeglut glutMainLoopEvent
        clock = loop.begin_frame()
        d = clock - lastclock
        lastclock = clock
        controller.onUpdate(d)
        controller.draw()
        loop.end_frame()
 