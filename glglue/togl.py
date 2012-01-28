#!/usr/bin/env python
# coding: utf-8

import OpenGL.Tk


class Widget(OpenGL.Tk.RawOpengl):
    def __init__(self, master, engine, *args, **kw):
        #super(Widget, self).__init__(master, *args, **kw)
        OpenGL.Tk.RawOpengl.__init__(self, master, *args, **kw)
        self.engine=engine
        self.bind('<Map>', self.onDraw)
        self.bind('<Expose>', self.onDraw)
        self.bind('<Configure>', self.onResize)
        self.bind('<ButtonPress-1>', lambda e: self.engine.onLeftDown(e.x, e.y) and self.onDraw())
        self.bind('<ButtonRelease-1>', lambda e: self.engine.onLeftUp(e.x, e.y) and self.onDraw())
        self.bind('<B1-Motion>', lambda e: self.engine.onMotion(e.x, e.y) and self.onDraw())
        self.bind('<ButtonPress-2>', lambda e: self.engine.onMiddleDown(e.x, e.y) and self.onDraw())
        self.bind('<ButtonRelease-2>', lambda e: self.engine.onMiddleUp(e.x, e.y) and self.onDraw())
        self.bind('<B2-Motion>', lambda e: self.engine.onMotion(e.x, e.y) and self.onDraw())
        self.bind('<ButtonPress-3>', lambda e: self.engine.onRightDown(e.x, e.y) and self.onDraw())
        self.bind('<ButtonRelease-3>', lambda e: self.engine.onRightUp(e.x, e.y) and self.onDraw())
        self.bind('<B3-Motion>', lambda e: self.engine.onMotion(e.x, e.y) and self.onDraw())

    def onDraw(self, *dummy):
        self.tk.call(self._w, 'makecurrent')
        self.update_idletasks()
        self.engine.draw()
        self.tk.call(self._w, 'swapbuffers')

    def onResize(self, event):
        self.engine.onResize(event.width, event.height)
        self.onDraw()


if __name__=="__main__":
    import sys
    if sys.version_info[0]<3:
        import Tkinter as tkinter
    else:
        import tkinter
    import glglue.sample
    class Frame(tkinter.Frame):
        def __init__(self, width, height, master=None, **kw):
            #super(Frame, self).__init__(master, **kw)
            tkinter.Frame.__init__(self, master, **kw)
            # setup opengl widget
            self.controller=glglue.sample.SampleController()
            self.glwidget=Widget(
                    self, self.controller, width=width, height=height)
            self.glwidget.pack(fill=tkinter.BOTH, expand=True)
            # event binding(require focus)
            self.bind('<Key>', self.onKeyDown)
            self.bind('<MouseWheel>', lambda e: self.controller.onWheel(-e.delta) and self.glwidget.onDraw())

        def onKeyDown(self, event):
            key=event.keycode
            if key==27:
                # Escape
                sys.exit()
            if key==81:
                # q
                sys.exit()
            else:
                print("keycode: %d" % key)

    f = Frame(width=600, height=600)
    f.pack(fill=tkinter.BOTH, expand=True)
    f.focus_set()
    f.mainloop()

