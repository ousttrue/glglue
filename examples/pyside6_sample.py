# coding: utf-8
"""
pip install pyside6
"""
from PySide6 import QtWidgets


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(None)
        import glglue.pyside6
        from glglue.scene.sample import SampleScene

        self.scene = SampleScene()

        self.glwidget = glglue.pyside6.Widget(self, render_gl=self.scene.render)
        self.setCentralWidget(self.glwidget)


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
