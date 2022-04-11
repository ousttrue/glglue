# coding: utf-8
'''
# glut
require pyOpenGL + glut.dll
require pyOpenGL + freeglut.dll

# glut install on Windows

* glut.dllもしくはfreeglut.dllを入手(vcpkgでビルドするのおすすめ)
* Python.exeと同じフォルダにコピーするか環境変数PATHを設定する
'''
import glglue.basecontroller


class Controller(glglue.basecontroller.BaseController):
    def __init__(self):
        super().__init__()

    def onUpdate(self, time_delta) -> bool:
        return False

    def onLeftDown(self, x: int, y: int) -> bool:
        return False

    def onLeftUp(self, x: int, y: int) -> bool:
        return False

    def onMiddleDown(self, x: int, y: int) -> bool:
        return False

    def onMiddleUp(self, x: int, y: int) -> bool:
        return False

    def onRightDown(self, x: int, y: int) -> bool:
        return False

    def onRightUp(self, x: int, y: int) -> bool:
        return False

    def onMotion(self, x: int, y: int) -> bool:
        return False

    def onResize(self, w: int, h: int) -> bool:
        return False

    def onWheel(self, d: int) -> bool:
        return False

    def onKeyDown(self, *args: str) -> bool:
        return False

    def draw(self) -> None:
        pass


def main():
    import glglue.glut
    controller = Controller()

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


if __name__ == "__main__":
    main()
