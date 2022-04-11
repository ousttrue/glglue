#
# pip install pyside6
#
from PySide6 import QtWidgets
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


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # setup opengl widget
        self.controller = Controller()
        import glglue.pyside6
        import glglue.utils
        self.glwidget = glglue.pyside6.Widget(
            self, self.controller, glglue.utils.get_desktop_scaling_factor())
        self.setCentralWidget(self.glwidget)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
