import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from .basecontroller import BaseController


class GLArea(Gtk.GLArea):
    def __init__(self, controller: BaseController, dpi_scale=1.0) -> None:
        super().__init__()
        self.controller = controller
        self.connect("render", self.on_draw)

    def on_draw(self, widget, *args):
        self.controller.draw()
