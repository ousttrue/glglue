import logging
import sys
import tkinter
import glglue.tk_frame
import glglue.scene.sample


LOGGER = logging.getLogger(__name__)


class Frame(tkinter.Frame):
    def __init__(self, master, *, width, height, **kw):  # type: ignore
        super(Frame, self).__init__(master, **kw)  # type: ignore

        # setup opengl widget
        self.scene = glglue.scene.sample.SampleScene()
        self.glwidget = glglue.tk_frame.TkGlFrame(
            self, self.scene.render, width=width, height=height
        )
        self.glwidget.pack(fill=tkinter.BOTH, expand=True)
        # event binding(require focus)
        self.bind("<Key>", self.onKeyDown)  # type: ignore
        self.bind(
            "<MouseWheel>",
            lambda e: self.glwidget.status.set_wheel(-e.delta),
        )

    def onKeyDown(self, event) -> None:  # type: ignore
        key = event.keycode  # type: ignore
        if key == 27:
            # Escape
            sys.exit()
        if key == 81:
            # q
            sys.exit()
        else:
            LOGGER.debug(f"keycode: {key}")


def main():
    logging.basicConfig(
        format="[%(levelname)s] %(name)s.%(funcName)s: %(message)s", level=logging.DEBUG
    )

    root = tkinter.Tk()
    app = Frame(root, width=320, height=200)
    app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.mainloop()


if __name__ == "__main__":
    main()
