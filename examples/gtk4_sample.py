import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

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


class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)  # type: ignore
        import glglue.gtk4

        self.glWidget = glglue.gtk4.GLArea(render)
        self.set_child(self.glWidget)


def on_activate(app: Gtk.Application):
    window = Window(app)
    window.present()


def main():
    app = Gtk.Application()
    app.connect("activate", on_activate)
    app.run()  # type: ignore


if __name__ == "__main__":
    main()
