import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        from glglue.scene.triangle import TriangleScene

        self.scene = TriangleScene()

        import glglue.gtk3

        self.glWidget = glglue.gtk3.GLArea(self.scene.render)
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
