import win32con
import sys
from ctypes import *
from OpenGL.GL import *

##############################################################################
# Windows types
##############################################################################
def ErrorIfZero(handle):
    if handle == 0:
        raise WinError()
    else:
        return handle

def LOWORD(n):
    return n & 0xFFFF

def HIWORD(n):
    return (n>>16)&0XFFFF

WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)

win32con.PFD_TYPE_RGBA =       0
win32con.PFD_TYPE_COLORINDEX = 1
win32con.PFD_MAIN_PLANE =      0
win32con.PFD_OVERLAY_PLANE =   1
win32con.PFD_UNDERLAY_PLANE =  (-1)
win32con.PFD_DOUBLEBUFFER =           0x00000001
win32con.PFD_STEREO =                 0x00000002
win32con.PFD_DRAW_TO_WINDOW =         0x00000004
win32con.PFD_DRAW_TO_BITMAP =         0x00000008
win32con.PFD_SUPPORT_GDI =            0x00000010
win32con.PFD_SUPPORT_OPENGL =         0x00000020
win32con.PFD_GENERIC_FORMAT =         0x00000040
win32con.PFD_NEED_PALETTE =           0x00000080
win32con.PFD_NEED_SYSTEM_PALETTE =    0x00000100
win32con.PFD_SWAP_EXCHANGE =          0x00000200
win32con.PFD_SWAP_COPY =              0x00000400
win32con.PFD_SWAP_LAYER_BUFFERS =     0x00000800
win32con.PFD_GENERIC_ACCELERATED =    0x00001000
win32con.PFD_DEPTH_DONTCARE =         0x20000000
win32con.PFD_DOUBLEBUFFER_DONTCARE =  0x40000000
win32con.PFD_STEREO_DONTCARE =        0x80000000

class WNDCLASS(Structure):
    _fields_ = [('style', c_uint),
            ('lpfnWndProc', WNDPROC),
            ('cbClsExtra', c_int),
            ('cbWndExtra', c_int),
            ('hInstance', c_int),
            ('hIcon', c_int),
            ('hCursor', c_int),
            ('hbrBackground', c_int),
            ('lpszMenuName', c_char_p),
            ('lpszClassName', c_char_p)]

class CREATESTRUCT(Structure):
    _fields_ = [('lpCreateParams', c_void_p),
            ('hInstance', c_int),
            ('hMenu', c_int),
            ('hwndParent', c_int),
            ('cy', c_int),
            ('cx', c_int),
            ('y', c_int),
            ('x', c_int),
            ('style', c_int),
            ('lpszName', c_char_p),
            ('lpszClass', c_char_p),
            ('dwExStyle', c_int)]

class PIXELFORMATDESCRIPTOR(Structure):
    _fields_ = [
            ('nSize', c_ushort),
            ('nVersion', c_ushort),
            ('dwFlags', c_ulong),
            ('iPixelType', c_ubyte),
            ('cColorBits', c_ubyte),
            ('cRedBits', c_ubyte),
            ('cRedShift', c_ubyte),
            ('cGreenBits', c_ubyte),
            ('cGreenShift', c_ubyte),
            ('cBlueBits', c_ubyte),
            ('cBlueShift', c_ubyte),
            ('cAlphaBits', c_ubyte),
            ('cAlphaShift', c_ubyte),
            ('cAccumBits', c_ubyte),
            ('cAccumRedBits', c_ubyte),
            ('cAccumGreenBits', c_ubyte),
            ('cAccumBlueBits', c_ubyte),
            ('cAccumAlphaBits', c_ubyte),
            ('cDepthBits', c_ubyte),
            ('cStencilBits', c_ubyte),
            ('cAuxBuffers', c_ubyte),
            ('iLayerType', c_ubyte),
            ('bReserved', c_ubyte),
            ('dwLayerMask', c_ulong),
            ('dwVisibleMask', c_ulong),
            ('dwDamageMask', c_ulong),
            ]

class RECT(Structure):
    _fields_ = [('left', c_long),
                ('top', c_long),
                ('right', c_long),
                ('bottom', c_long)]

class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', c_int),
                ('fErase', c_int),
                ('rcPaint', RECT),
                ('fRestore', c_int),
                ('fIncUpdate', c_int),
                ('rgbReserved', c_char * 32)]

class POINT(Structure):
    _fields_ = [('x', c_long),
                ('y', c_long)]
    
class MSG(Structure):
    _fields_ = [('hwnd', c_int),
                ('message', c_uint),
                ('wParam', c_int),
                ('lParam', c_int),
                ('time', c_int),
                ('pt', POINT)]

CreateWindowEx = windll.user32.CreateWindowExA
CreateWindowEx.argtypes = [
        c_int, c_char_p, c_char_p, 
        c_int, c_int, c_int, c_int, 
        c_int, c_int, c_int, c_int,
        py_object
        ]
CreateWindowEx.restype = ErrorIfZero

SetWindowLongPtr = windll.user32.SetWindowLongA
SetWindowLongPtr.argtypes = [
        c_int, c_int, c_void_p
        ]
SetWindowLongPtr.restype = c_void_p

GetWindowLongPtr = windll.user32.GetWindowLongA
GetWindowLongPtr.argtypes = [
        c_int, c_int
        ]
GetWindowLongPtr.restype = c_void_p

GetDC=windll.user32.GetDC
GetDC.argtypes = [
        c_int
        ]
GetWindowLongPtr.restype = ErrorIfZero

ChoosePixelFormat = windll.gdi32.ChoosePixelFormat
ChoosePixelFormat.argtypes=[
    c_int, c_void_p
]
ChoosePixelFormat.restype=ErrorIfZero

SetPixelFormat=windll.gdi32.SetPixelFormat
SetPixelFormat.argtypes=[
    c_int, c_int, c_void_p,
]
SetPixelFormat.restype=ErrorIfZero

SwapBuffers=windll.gdi32.SwapBuffers
SwapBuffers.argtypes=[
        c_int,
        ]
SwapBuffers.restype=ErrorIfZero

wglCreateContext=windll.opengl32.wglCreateContext
wglCreateContext.argtypes=[
    c_int,
]
wglCreateContext.restype=ErrorIfZero

wglMakeCurrent=windll.opengl32.wglMakeCurrent
wglMakeCurrent.argtypes=[
    c_int, c_int,
]
wglMakeCurrent.restype=ErrorIfZero

DefWindowProc=windll.user32.DefWindowProcA
DefWindowProc.argtypes=[
        c_int, c_int, c_int, c_int
        ]
DefWindowProc.restype=c_int

timeGetTime=windll.winmm.timeGetTime
timeGetTime.argtypes=[]
timeGetTime.restype=c_ulong

##############################################################################
# api class
##############################################################################
class Window(object):
    def __init__(self):
        self.hwnd=None
        self.hrc=None
        self.controller=None
        self.ptrs={}
        self.callbacks={
                win32con.WM_PAINT: self.onPaint,
                win32con.WM_SIZE: self.onSize,
                win32con.WM_ERASEBKGND: self.onErasebkgnd,
                win32con.WM_DESTROY: self.onDestroy,
                win32con.WM_LBUTTONDOWN: self.onLeftDown,
                win32con.WM_LBUTTONUP: self.onLeftUp,
                win32con.WM_MBUTTONDOWN: self.onMiddleDown,
                win32con.WM_MBUTTONUP: self.onMiddleUp,
                win32con.WM_RBUTTONDOWN: self.onRightDown,
                win32con.WM_RBUTTONUP: self.onRightUp,
                win32con.WM_MOUSEMOVE: self.onMouseMove,
                win32con.WM_MOUSEWHEEL: self.onMouseWheel,
                win32con.WM_KEYDOWN: self.onKeyDown,
                }

    def finalize(self):
        print('finalize', self.__class__)

    def Redraw(self):
        windll.user32.InvalidateRect(c_int(self.hwnd), c_int(0), c_int(0))

    def Show(self):
        windll.user32.ShowWindow(c_int(self.hwnd), 
                c_int(win32con.SW_SHOWNORMAL))
        windll.user32.UpdateWindow(c_int(self.hwnd))

    def SetLongPtr(self, key, value):
        self.ptrs[key]=value
        SetWindowLongPtr(c_int(self.hwnd), key, value);

    def onPaint(self, hwnd, message, wParam, lParam):
        #sys.stderr.write("WM_PAINT\n")
        if self.hrc and self.controller:
            ps = PAINTSTRUCT()
            hdc = windll.user32.BeginPaint(c_int(hwnd), byref(ps))
            self.controller.draw()
            SwapBuffers(hdc)
            windll.user32.EndPaint(c_int(hwnd), byref(ps))
        return 0

    def onSize(self, hwnd, message, wParam, lParam):
        #sys.stderr.write("WM_SIZE\n")
        if self.controller:
            w=LOWORD(lParam)
            h=HIWORD(lParam)
            self.controller.onResize(w, h)
        return 0

    def onErasebkgnd(self, hwnd, message ,wParam, lParam):
        return 0

    def onDestroy(self, hwnd, message, wParam, lParam):
            #sys.stderr.write("WM_DESTROY\n")
            windll.user32.PostQuitMessage(0)
            return 0

    def onKeyDown(self, hwnd, message, wParam, lParam):
        if self.controller:
            if self.controller.onKeyDown(wParam):
                self.Redraw()
        return 0

    def onMouseMove(self, hwnd, message, wParam, lParam):
        if self.controller:
            x=LOWORD(lParam);
            y=HIWORD(lParam);
            if self.controller.onMotion(x, y):
                self.Redraw()
        return 0

    def onMouseWheel(self, hwnd, message, wParam, lParam):
        if self.controller:
            d=HIWORD(wParam);
            if self.controller.onWheel(d>32767 and 65536-d or -d):
                self.Redraw()
        return 0

    def onLeftUp(self, hwnd, message, wParam, lParam):
        if self.controller:
            x=LOWORD(lParam);
            y=HIWORD(lParam);
            if self.controller.onLeftUp(x, y):
                self.Redraw()
        return 0

    def onLeftDown(self, hwnd, message, wParam, lParam):
        if self.controller:
            x=LOWORD(lParam);
            y=HIWORD(lParam);
            if self.controller.onLeftDown(x, y):
                self.Redraw()
        return 0

    def onMiddleUp(self, hwnd, message, wParam, lParam):
        if self.controller:
            x=LOWORD(lParam);
            y=HIWORD(lParam);
            if self.controller.onMiddleUp(x, y):
                self.Redraw()
        return 0

    def onMiddleDown(self, hwnd, message, wParam, lParam):
        if self.controller:
            x=LOWORD(lParam);
            y=HIWORD(lParam);
            if self.controller.onMiddleDown(x, y):
                self.Redraw()
        return 0

    def onRightUp(self, hwnd, message, wParam, lParam):
        if self.controller:
            x=LOWORD(lParam);
            y=HIWORD(lParam);
            if self.controller.onRightUp(x, y):
                self.Redraw()
        return 0

    def onRightDown(self, hwnd, message, wParam, lParam):
        if self.controller:
            x=LOWORD(lParam);
            y=HIWORD(lParam);
            if self.controller.onRightDown(x, y):
                self.Redraw()
        return 0

    def WndProc(self, hwnd, message, wParam, lParam):
        if message in self.callbacks:
            return self.callbacks[message](hwnd, message, wParam, lParam)
        else:
            return DefWindowProc(hwnd, message, wParam, lParam)

    def createGLContext(self, bits):
        hdc=GetDC(self.hwnd)

        pfd=PIXELFORMATDESCRIPTOR()
        pfd.nsize=sizeof(PIXELFORMATDESCRIPTOR)
        pfd.nVersion=1
        pfd.dwFlags=(
                win32con.PFD_DRAW_TO_WINDOW |
                win32con.PFD_SUPPORT_OPENGL |
                win32con.PFD_DOUBLEBUFFER)
        pfd.iPixelType=win32con.PFD_TYPE_RGBA
        pfd.cColorBits=bits
        pfd.cRedBits=0
        pfd.cRedShift=0
        pfd.cGreenBits=0
        pfd.cGreenShift=0
        pfd.cBlueBits=0
        pfd.cBlueShift=0
        pfd.cAlphaBits=0
        pfd.cAlphaShift=0
        pfd.cAccumBits=0
        pfd.cAccumRedBits=0
        pfd.cAccumGreenBits=0
        pfd.cAccumBlueBits=0
        pfd.cAccumAlphaBits=0
        pfd.cDepthBits=bits
        pfd.cStencilBits=0
        pfd.cAuxBuffers=0
        pfd.iLayerType=win32con.PFD_MAIN_PLANE
        pfd.bReserved=0
        pfd.dwLayerMask=0
        pfd.dwVisibleMask=0
        pfd.dwDamageMask=0

        pixelFormat=ChoosePixelFormat(hdc, byref(pfd))
        SetPixelFormat(hdc, pixelFormat, byref(pfd))

        self.hrc=wglCreateContext(hdc)
        wglMakeCurrent(hdc, self.hrc)

    @staticmethod
    def WndProcProxy(hwnd, message, wParam, lParam):
        #sys.stderr.write("Window::WndProcProxy\n")
        p=GetWindowLongPtr(hwnd, win32con.GWL_USERDATA)
        window=cast(p, py_object)
        return window.value.WndProc(hwnd, message, wParam, lParam)
        

class WindowFactory(object):
    def __init__(self):
        self.classes=[]
        self.windows=[]
        self.wndclass=self.register_class(b"MainWin")

    def __del__(self):
        self.finalize()

    def finalize(self):
        for w in self.windows:
            w.value.finalize()
        print('finalize', self.__class__)

    def register_class(self, className):
        """
        RegisterClassA
        """
        # Define Window Class
        wndclass = WNDCLASS()
        wndclass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndclass.lpfnWndProc = WNDPROC(WindowFactory.WndProc)
        wndclass.cbClsExtra = wndclass.cbWndExtra = 0
        wndclass.hInstance = windll.kernel32.GetModuleHandleA(
                c_int(win32con.NULL))
        wndclass.hIcon = windll.user32.LoadIconA(
                c_int(win32con.NULL), c_int(win32con.IDI_APPLICATION))
        wndclass.hCursor = windll.user32.LoadCursorA(
                c_int(win32con.NULL), c_int(win32con.IDC_ARROW))
        wndclass.hbrBackground = windll.gdi32.GetStockObject(
                c_int(win32con.WHITE_BRUSH))
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = className
        # Register Window Class
        if not windll.user32.RegisterClassA(byref(wndclass)):
            raise WinError()
        self.classes.append(wndclass)
        return wndclass

    def create(self, klass, **kw):
        width='width' in kw and kw['width'] or win32con.CW_USEDEFAULT
        height='height' in kw and kw['height'] or win32con.CW_USEDEFAULT
        wndclass='wndclass' in kw and kw['wndclass'] or self.wndclass
        title='title' in kw and kw['title'] or b"glglue.wgl"

        window=klass()
        pywindow=py_object(window)
        hwnd=CreateWindowEx(0,
                              wndclass.lpszClassName,
                              title,
                              win32con.WS_OVERLAPPEDWINDOW,
                              win32con.CW_USEDEFAULT,
                              win32con.CW_USEDEFAULT,
                              width,
                              height,
                              win32con.NULL,
                              win32con.NULL,
                              wndclass.hInstance,
                              pywindow)
        self.windows.append(pywindow)
        return window

    def loop(self, window):
        msg = MSG()
        pMsg = pointer(msg)
        NULL = c_int(win32con.NULL)
        #while windll.user32.GetMessageA( pMsg, NULL, 0, 0) != 0:
        #    windll.user32.TranslateMessage(pMsg)
        #    windll.user32.DispatchMessageA(pMsg)
        lastCount=timeGetTime()
        while True:
            if windll.user32.PeekMessageA(pMsg, NULL, 0, 0, win32con.PM_NOREMOVE) != 0:
                if windll.user32.GetMessageA(pMsg, NULL, 0, 0)==0:
                    return msg.wParam
                windll.user32.TranslateMessage(pMsg)
                windll.user32.DispatchMessageA(pMsg)
            else:
                count=timeGetTime()
                d=count-lastCount
                if d>0:
                    #print d
                    window.controller.onUpdate(d)
                    window.Redraw()
                    lastCount=count

    @staticmethod
    def WndProc(hwnd, message, wParam, lParam):
        #sys.stderr.write("WindowFactory::WndProc\n")
        if message == win32con.WM_CREATE:
            lpcreatestruct=cast(lParam, POINTER(CREATESTRUCT))
            createstruct = lpcreatestruct.contents;
            window=cast(createstruct.lpCreateParams, py_object).value
            window.hwnd=hwnd
            window.SetLongPtr(win32con.GWL_USERDATA, 
                    createstruct.lpCreateParams)
            window.SetLongPtr(win32con.GWL_WNDPROC,
                    cast(WNDPROC(Window.WndProcProxy), c_void_p))
            return window.WndProc(hwnd, message, wParam, lParam)

        elif message == win32con.WM_DESTROY:
            windll.user32.PostQuitMessage(0)
            return 0
        
        return DefWindowProc(hwnd, message, wParam, lParam)


def mainloop(controller, **kw):
    factory=WindowFactory()
    window=factory.create(Window, **kw)
    window.createGLContext(16)
    window.controller=controller
    window.Show()
    import sys
    sys.exit(factory.loop(window))


if __name__=="__main__":
    import os
    if os.name!='nt':
        print("this script is windows only: "+os.name)
        sys.exit()
    import glglue.sample
    mainloop(glglue.sample.SampleController(), width=600, height=400)

