import gi
import traceback

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)  # type: ignore

        from glglue.scene.sample import SampleScene
        self.scene = SampleScene()

        import glglue.gtk4

        self.glWidget = glglue.gtk4.GLArea(self.scene.render)
        self.set_child(self.glWidget)


def on_activate(app: Gtk.Application):
    try:
        window = Window(app)
        window.present()
    except Exception as ex:
        traceback.print_exception(ex)
        app.quit()


def main():
    app = Gtk.Application()
    app.connect("activate", on_activate)
    app.run()  # type: ignore


if __name__ == "__main__":
    main()
