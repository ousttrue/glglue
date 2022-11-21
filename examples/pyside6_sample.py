import glglue.frame_input


def render(frame: glglue.frame_input.FrameInput):
    from OpenGL import GL

    GL.glViewport(0, 0, frame.width, frame.height)

    r = float(frame.x) / float(frame.width)
    g = 1 if frame.left_down else 0
    if frame.height == 0:
        return
    b = float(frame.y) / float(frame.height)
    GL.glClearColor(r, g, b, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

    GL.glFlush()


from PySide6 import QtWidgets


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(None)
        import glglue.pyside6

        self.glwidget = glglue.pyside6.Widget(self, render_gl=render)
        self.setCentralWidget(self.glwidget)


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
