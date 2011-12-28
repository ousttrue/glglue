# -*- coding: utf-8 -*-
import wx
import wx.glcanvas


class Widget(wx.glcanvas.GLCanvas):
    def __init__(self, parent, controller, *args, **kwargs):
        attribList = (wx.glcanvas.WX_GL_RGBA, # RGBA
                wx.glcanvas.WX_GL_DOUBLEBUFFER, # Double Buffered
                wx.glcanvas.WX_GL_DEPTH_SIZE, 32) # 32 bit
        super(Widget, self).__init__(parent, 
                attribList=attribList, *args, **kwargs)
        self.controller=controller
        # コールバック
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBG)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        self.controller.draw()
        self.SwapBuffers()
        event.Skip()
        return

    def OnResize(self, event):
        self.size = self.GetClientSize()

        if self.GetContext():
            self.SetCurrent()
            self.controller.onResize(self.size.width, self.size.height)
        self.Refresh()
        event.Skip()

    def OnEraseBG(self, event):
        pass # Do nothing, to avoid flashing on MSWin


if __name__=="__main__":
    import glglue.sample
    class Frame(wx.Frame):
        def __init__(self, parent, **kwargs):
            super(Frame, self).__init__(parent, **kwargs)
            # setup opengl widget
            self.controller=glglue.sample.SampleController()
            self.glwidget=Widget(self, self.controller)
            # packing
            sizer=wx.BoxSizer(wx.HORIZONTAL)
            self.SetSizer(sizer)
            sizer.Add(self.glwidget, 1, wx.EXPAND)

    app = wx.App(False)
    frame=Frame(None, title='glglue')
    frame.Show()
    app.MainLoop()

