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
    controller = Controller()

    import glglue.glfw
    loop = glglue.glfw.LoopManager(controller, title='glfw sample')

    lastCount = 0
    while True:
        count = loop.begin_frame()
        if not count:
            break
        d = count - lastCount
        lastCount = count
        if d > 0:
            controller.onUpdate(d)
            controller.draw()
            loop.end_frame()


if __name__ == "__main__":
    main()
