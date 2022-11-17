import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import glglue.basecontroller
from glglue.util import DummyScene


class Controller(glglue.basecontroller.BaseController):
    def __init__(self):
        super().__init__()
        self.scene = DummyScene()

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
        self.scene.resize(w, h)
        return False

    def onWheel(self, d: int) -> bool:
        return False

    def onKeyDown(self, *args: str) -> bool:
        return False

    def draw(self) -> None:
        self.scene.draw()


class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        # setup opengl widget
        self.controller = Controller()

        import glglue.gtk3
        import glglue.util

        self.glWidget = glglue.gtk3.GLArea(
            self.controller, glglue.util.get_desktop_scaling_factor()
        )
        self.add(self.glWidget)


def on_activate(app: Gtk.Application):
    window = Window(app)
    window.show_all()


def main():
    app = Gtk.Application()
    app.connect("activate", on_activate)
    app.run()


if __name__ == "__main__":
    main()
