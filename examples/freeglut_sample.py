# coding: utf-8
"""
> git clone https://github.com/FreeGLUTProject/freeglut.git


# glut
require pyOpenGL + glut.dll
require pyOpenGL + freeglut.dll

# glut install on Windows

* glut.dllもしくはfreeglut.dllを入手(vcpkgでビルドするのおすすめ)
* Python.exeと同じフォルダにコピーするか環境変数PATHを設定する
"""


def main():
    import glglue.glut
    from glglue.scene.triangle import TriangleScene

    scene = TriangleScene()

    # manual loop
    loop = glglue.glut.LoopManager()
    while True:
        # require freeglut glutMainLoopEvent
        frame = loop.begin_frame()
        if not frame:
            break
        scene.render(frame)
        loop.end_frame()


if __name__ == "__main__":
    main()
