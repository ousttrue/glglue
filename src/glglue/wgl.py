﻿from logging import getLogger
logger = getLogger(__name__)

import sys
sys.path.append('..')
sys.path.append('.')
from ctypes import *
from ctypes.wintypes import *

from OpenGL.GL import *
from glglue import win32con


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
    return (n >> 16) & 0XFFFF


WNDPROC = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)

win32con.PFD_TYPE_RGBA = 0
win32con.PFD_TYPE_COLORINDEX = 1
win32con.PFD_MAIN_PLANE = 0
win32con.PFD_OVERLAY_PLANE = 1
win32con.PFD_UNDERLAY_PLANE = (-1)
win32con.PFD_DOUBLEBUFFER = 0x00000001
win32con.PFD_STEREO = 0x00000002
win32con.PFD_DRAW_TO_WINDOW = 0x00000004
win32con.PFD_DRAW_TO_BITMAP = 0x00000008
win32con.PFD_SUPPORT_GDI = 0x00000010
win32con.PFD_SUPPORT_OPENGL = 0x00000020
win32con.PFD_GENERIC_FORMAT = 0x00000040
win32con.PFD_NEED_PALETTE = 0x00000080
win32con.PFD_NEED_SYSTEM_PALETTE = 0x00000100
win32con.PFD_SWAP_EXCHANGE = 0x00000200
win32con.PFD_SWAP_COPY = 0x00000400
win32con.PFD_SWAP_LAYER_BUFFERS = 0x00000800
win32con.PFD_GENERIC_ACCELERATED = 0x00001000
win32con.PFD_DEPTH_DONTCARE = 0x20000000
win32con.PFD_DOUBLEBUFFER_DONTCARE = 0x40000000
win32con.PFD_STEREO_DONTCARE = 0x80000000

WGL_ARB_create_context = 1
WGL_CONTEXT_DEBUG_BIT_ARB = 0x00000001
WGL_CONTEXT_FORWARD_COMPATIBLE_BIT_ARB = 0x00000002
WGL_CONTEXT_MAJOR_VERSION_ARB = 0x2091
WGL_CONTEXT_MINOR_VERSION_ARB = 0x2092
WGL_CONTEXT_LAYER_PLANE_ARB = 0x2093
WGL_CONTEXT_FLAGS_ARB = 0x2094
WGL_CONTEXT_PROFILE_MASK_ARB = 0x9126
WGL_CONTEXT_CORE_PROFILE_BIT_ARB = 0x00000001
WGL_CONTEXT_COMPATIBILITY_PROFILE_BIT_ARB = 0x00000002


class WNDCLASS(Structure):
    _fields_ = [('style', c_uint), ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int), ('cbWndExtra', c_int),
                ('hInstance', HANDLE), ('hIcon', HANDLE), ('hCursor', HANDLE),
                ('hbrBackground', HANDLE), ('lpszMenuName', LPCSTR),
                ('lpszClassName', LPCSTR)]


class CREATESTRUCT(Structure):
    _fields_ = [('lpCreateParams', c_void_p), ('hInstance', HANDLE),
                ('hMenu', HANDLE), ('hwndParent', HWND), ('cy', c_int),
                ('cx', c_int), ('y', c_int), ('x', c_int), ('style', c_int),
                ('lpszName', LPCSTR), ('lpszClass', LPCSTR),
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
    _fields_ = [('left', c_long), ('top', c_long), ('right', c_long),
                ('bottom', c_long)]


class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', HDC), ('fErase', BOOL), ('rcPaint', RECT),
                ('fRestore', BOOL), ('fIncUpdate', BOOL),
                ('rgbReserved', c_char * 32)]


class POINT(Structure):
    _fields_ = [('x', c_long), ('y', c_long)]


class MSG(Structure):
    _fields_ = [('hwnd', HWND), ('message', c_uint), ('wParam', WPARAM),
                ('lParam', LPARAM), ('time', c_int), ('pt', POINT)]


ShowWindow = windll.user32.ShowWindow
ShowWindow.argtypes = [HWND, c_int]
ShowWindow.restype = BOOL

RegisterClass = windll.user32.RegisterClassA
RegisterClass.argtypes = [c_void_p]
RegisterClass.restype = ATOM

CreateWindowEx = windll.user32.CreateWindowExA
CreateWindowEx.argtypes = [
    c_int, LPCSTR, LPCSTR, c_int, c_int, c_int, c_int, c_int, HWND, HANDLE,
    HANDLE, py_object
]
CreateWindowEx.restype = HWND

if sys.maxsize > 2**32:
    # 64bit
    SetWindowLongPtr = windll.user32.SetWindowLongPtrA
    SetWindowLongPtr.argtypes = [HWND, c_int, c_void_p]
    SetWindowLongPtr.restype = c_void_p

    GetWindowLongPtr = windll.user32.GetWindowLongPtrA
    GetWindowLongPtr.argtypes = [HWND, c_int]
    GetWindowLongPtr.restype = c_void_p
else:
    # 64bit
    SetWindowLongPtr = windll.user32.SetWindowLongA
    SetWindowLongPtr.argtypes = [HWND, c_int, c_void_p]
    SetWindowLongPtr.restype = c_void_p

    GetWindowLongPtr = windll.user32.GetWindowLongA
    GetWindowLongPtr.argtypes = [HWND, c_int]
    GetWindowLongPtr.restype = c_void_p

GetDC = windll.user32.GetDC
GetDC.argtypes = [HWND]

BeginPaint = windll.user32.BeginPaint
BeginPaint.argtypes = [HWND, c_void_p]
BeginPaint.restype = HDC

EndPaint = windll.user32.EndPaint
EndPaint.argtypes = [HWND, c_void_p]
EndPaint.restype = HDC

ChoosePixelFormat = windll.gdi32.ChoosePixelFormat
ChoosePixelFormat.argtypes = [HDC, c_void_p]
ChoosePixelFormat.restype = ErrorIfZero

SetPixelFormat = windll.gdi32.SetPixelFormat
SetPixelFormat.argtypes = [
    HDC,
    c_int,
    c_void_p,
]
SetPixelFormat.restype = ErrorIfZero

SwapBuffers = windll.gdi32.SwapBuffers
SwapBuffers.argtypes = [
    HDC,
]
SwapBuffers.restype = ErrorIfZero

wglCreateContext = windll.opengl32.wglCreateContext
wglCreateContext.argtypes = [
    HDC,
]
wglCreateContext.restype = ErrorIfZero

wglDeleteContext = windll.opengl32.wglDeleteContext

wglMakeCurrent = windll.opengl32.wglMakeCurrent
wglMakeCurrent.argtypes = [
    HDC,
    HANDLE,
]
wglMakeCurrent.restype = ErrorIfZero

wglGetProcAddress = windll.opengl32.wglGetProcAddress
wglGetProcAddress.argtypes = [c_void_p]
wglGetProcAddress.restype = ErrorIfZero

DefWindowProc = windll.user32.DefWindowProcA
DefWindowProc.argtypes = [HWND, c_int, WPARAM, LPARAM]
DefWindowProc.restype = c_int

timeGetTime = windll.winmm.timeGetTime
timeGetTime.argtypes = []
timeGetTime.restype = c_ulong

##############################################################################
# api class
##############################################################################


class Window(object):
    def __init__(self):
        self.hwnd = None
        self.hrc = None
        self.controller = None
        self.ptrs = {}
        self.callbacks = {
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
        logger.debug('finalize %s', self.__class__)

    def Redraw(self):
        windll.user32.InvalidateRect(self.hwnd, c_int(0), c_int(0))

    def Show(self):
        ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
        windll.user32.UpdateWindow(self.hwnd)

    def SetLongPtr(self, hwnd, key, value):
        self.ptrs[key] = value
        SetWindowLongPtr(hwnd, key, value)

    def onPaint(self, hwnd, message, wParam, lParam):
        ps = PAINTSTRUCT()
        hdc = BeginPaint(hwnd, byref(ps))
        # if self.hrc and self.controller:
        #     self.controller.draw()
        #     SwapBuffers(hdc)
        EndPaint(hwnd, byref(ps))
        return 0

    def onSize(self, hwnd, message, wParam, lParam):
        w = LOWORD(lParam)
        h = HIWORD(lParam)
        # logger.debug("WM_SIZE %d x %d %s" % (w, h, self.controller))
        if self.controller:
            self.controller.onResize(w, h)
        return 0

    def onErasebkgnd(self, hwnd, message, wParam, lParam):
        return 0

    def onDestroy(self, hwnd, message, wParam, lParam):
        # sys.stderr.write("WM_DESTROY\n")
        windll.user32.PostQuitMessage(0)
        return 0

    def onKeyDown(self, hwnd, message, wParam, lParam):
        if self.controller:
            if wParam >= 65 and wParam <= 90:
                # lower
                if self.controller.onKeyDown(wParam + 32):
                    self.Redraw()
            else:
                if self.controller.onKeyDown(wParam):
                    self.Redraw()
        return 0

    def onMouseMove(self, hwnd, message, wParam, lParam):
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onMotion(x, y):
                self.Redraw()
        return 0

    def onMouseWheel(self, hwnd, message, wParam, lParam):
        if self.controller:
            d = HIWORD(wParam)
            if self.controller.onWheel(d > 32767 and 65536 - d or -d):
                self.Redraw()
        return 0

    def onLeftUp(self, hwnd, message, wParam, lParam):
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onLeftUp(x, y):
                self.Redraw()
        return 0

    def onLeftDown(self, hwnd, message, wParam, lParam):
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onLeftDown(x, y):
                self.Redraw()
        return 0

    def onMiddleUp(self, hwnd, message, wParam, lParam):
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onMiddleUp(x, y):
                self.Redraw()
        return 0

    def onMiddleDown(self, hwnd, message, wParam, lParam):
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onMiddleDown(x, y):
                self.Redraw()
        return 0

    def onRightUp(self, hwnd, message, wParam, lParam):
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onRightUp(x, y):
                self.Redraw()
        return 0

    def onRightDown(self, hwnd, message, wParam, lParam):
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onRightDown(x, y):
                self.Redraw()
        return 0

    def WndProc(self, hwnd, message, wParam, lParam):
        if message in self.callbacks:
            return self.callbacks[message](hwnd, message, wParam, lParam)
        else:
            return DefWindowProc(hwnd, message, wParam, lParam)

    def createGLContext(self, bits, version=None, profile='compatibility'):
        hdc = GetDC(self.hwnd)

        pfd = PIXELFORMATDESCRIPTOR()
        pfd.nsize = sizeof(PIXELFORMATDESCRIPTOR)
        pfd.nVersion = 1
        pfd.dwFlags = (win32con.PFD_DRAW_TO_WINDOW
                       | win32con.PFD_SUPPORT_OPENGL
                       | win32con.PFD_DOUBLEBUFFER)
        pfd.iPixelType = win32con.PFD_TYPE_RGBA
        pfd.cColorBits = bits
        pfd.cRedBits = 0
        pfd.cRedShift = 0
        pfd.cGreenBits = 0
        pfd.cGreenShift = 0
        pfd.cBlueBits = 0
        pfd.cBlueShift = 0
        pfd.cAlphaBits = 0
        pfd.cAlphaShift = 0
        pfd.cAccumBits = 0
        pfd.cAccumRedBits = 0
        pfd.cAccumGreenBits = 0
        pfd.cAccumBlueBits = 0
        pfd.cAccumAlphaBits = 0
        pfd.cDepthBits = bits
        pfd.cStencilBits = 2
        pfd.cAuxBuffers = 0
        pfd.iLayerType = win32con.PFD_MAIN_PLANE
        pfd.bReserved = 0
        pfd.dwLayerMask = 0
        pfd.dwVisibleMask = 0
        pfd.dwDamageMask = 0

        pixelFormat = ChoosePixelFormat(hdc, byref(pfd))
        SetPixelFormat(hdc, pixelFormat, byref(pfd))

        self.hrc = wglCreateContext(hdc)
        wglMakeCurrent(hdc, self.hrc)

        if version or profile:
            p = wglGetProcAddress("wglCreateContextAttribsARB".encode('utf-8'))
            wglCreateContextAttribsARB = WINFUNCTYPE(c_void_p, HDC, c_void_p,
                                                     POINTER(c_int))(p)

            attribs = []
            if version:
                major, minor = version.split('.')
                attribs.append(WGL_CONTEXT_MAJOR_VERSION_ARB)
                attribs.append(int(major))
                attribs.append(WGL_CONTEXT_MINOR_VERSION_ARB)
                attribs.append(int(minor))

            attribs.append(WGL_CONTEXT_FLAGS_ARB)
            attribs.append(0)

            if profile == 'core':
                attribs.append(WGL_CONTEXT_PROFILE_MASK_ARB)
                attribs.append(WGL_CONTEXT_CORE_PROFILE_BIT_ARB)
            elif profile == 'compatibility':
                attribs.append(WGL_CONTEXT_PROFILE_MASK_ARB)
                attribs.append(WGL_CONTEXT_COMPATIBILITY_PROFILE_BIT_ARB)

            attribs.append(0)

            hrc = wglCreateContextAttribsARB(
                hdc, None, (ctypes.c_int * len(attribs))(*attribs))
            wglDeleteContext(self.hrc)
            self.hrc = hrc
            wglMakeCurrent(hdc, self.hrc)

        for x in [
                'GL_VERSION',
                #'GL_EXTENSIONS',
                'GL_SHADING_LANGUAGE_VERSION',
                'GL_RENDERER'
        ]:
            logger.info('%s: %s', x, glGetString(globals()[x]))

        # GL_ARB_compatibility
        profile = None
        try:
            extensions = glGetString(GL_EXTENSIONS).decode('ascii').split()
            if 'GL_ARB_compatibility' in extensions:
                profile = 'COMPATIBILITY'
        except OpenGL.error.GLerror as ex:
            profile = 'CORE'
        logger.info('OpenGL%d.%d %s', glGetInteger(GL_MAJOR_VERSION),
                    glGetInteger(GL_MINOR_VERSION), profile)

    @staticmethod
    def WndProcProxy(hwnd, message, wParam, lParam):
        # sys.stderr.write("Window::WndProcProxy\n")
        p = GetWindowLongPtr(hwnd, win32con.GWL_USERDATA)
        window = cast(p, py_object)
        return window.value.WndProc(hwnd, message, wParam, lParam)


class WindowFactory(object):
    def __init__(self):
        self.classes = []
        self.windows = []
        self.wndclass = self.register_class(b"MainWin")

    def __del__(self):
        self.finalize()

    def finalize(self):
        for w in self.windows:
            w.value.finalize()
        logger.debug('finalize %s', self.__class__)

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
            HANDLE(win32con.NULL))
        wndclass.hIcon = windll.user32.LoadIconA(
            HANDLE(win32con.NULL), LPCSTR(win32con.IDI_APPLICATION))
        wndclass.hCursor = windll.user32.LoadCursorA(
            HANDLE(win32con.NULL), LPCSTR(win32con.IDC_ARROW))
        # wndclass.hbrBackground = windll.gdi32.GetStockObject(
        #     c_int(win32con.WHITE_BRUSH))
        wndclass.hbrBackground = None
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = className
        # Register Window Class
        res = RegisterClass(byref(wndclass))
        # logger.debug(res)
        if not res:
            raise WinError()
        self.classes.append(wndclass)
        return wndclass

    def create(self, klass, **kw):
        width = 'width' in kw and kw['width'] or win32con.CW_USEDEFAULT
        height = 'height' in kw and kw['height'] or win32con.CW_USEDEFAULT
        wndclass = b'wndclass' in kw and kw['wndclass'] or self.wndclass
        title = b'title' in kw and kw['title'] or b"glglue.wgl"

        window = klass()
        pywindow = py_object(window)
        hwnd = CreateWindowEx(0, wndclass.lpszClassName, title,
                              win32con.WS_OVERLAPPEDWINDOW,
                              win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                              width, height, win32con.NULL, win32con.NULL,
                              wndclass.hInstance, pywindow)
        self.windows.append(pywindow)
        return window

    def loop(self, window):
        msg = MSG()
        pMsg = pointer(msg)
        NULL = c_int(win32con.NULL)
        # while windll.user32.GetMessageA( pMsg, NULL, 0, 0) != 0:
        #    windll.user32.TranslateMessage(pMsg)
        #    windll.user32.DispatchMessageA(pMsg)
        lastCount = timeGetTime()
        while True:
            if windll.user32.PeekMessageA(pMsg, NULL, 0, 0,
                                          win32con.PM_NOREMOVE) != 0:
                if windll.user32.GetMessageA(pMsg, NULL, 0, 0) == 0:
                    return msg.wParam
                windll.user32.TranslateMessage(pMsg)
                windll.user32.DispatchMessageA(pMsg)
            else:
                count = timeGetTime()
                d = count - lastCount
                if d > 0:
                    window.controller.onUpdate(d)
                    window.Redraw()
                    lastCount = count

    @staticmethod
    def WndProc(hwnd, message, wParam, lParam):
        # sys.stderr.write("WindowFactory::WndProc\n")
        if message == win32con.WM_CREATE:
            lpcreatestruct = cast(lParam, POINTER(CREATESTRUCT))
            createstruct = lpcreatestruct.contents
            window = cast(createstruct.lpCreateParams, py_object).value
            window.hwnd = hwnd
            window.SetLongPtr(hwnd, win32con.GWL_USERDATA,
                              createstruct.lpCreateParams)
            window.SetLongPtr(hwnd, win32con.GWL_WNDPROC,
                              cast(WNDPROC(Window.WndProcProxy), c_void_p))
            return window.WndProc(hwnd, message, wParam, lParam)

        elif message == win32con.WM_DESTROY:
            windll.user32.PostQuitMessage(0)
            return 0

        return DefWindowProc(hwnd, message, wParam, lParam)


class LoopManager:
    def __init__(self, controller, **kw):
        self.controller = controller
        self.factory = WindowFactory()
        self.window = self.factory.create(Window, **kw)
        self.window.createGLContext(16,
                                    version=kw.get('version'),
                                    profile=kw.get('profile', 'compatibility'))
        self.window.controller = controller
        ShowWindow(self.window.hwnd, win32con.SW_SHOWNORMAL)
        self.msg = MSG()
        self.pMsg = pointer(self.msg)
        self.NULL = c_int(win32con.NULL)

    def begin_frame(self):
        while True:
            if windll.user32.PeekMessageA(self.pMsg, self.NULL, 0, 0,
                                          win32con.PM_NOREMOVE) != 0:
                if windll.user32.GetMessageA(self.pMsg, self.NULL, 0, 0) == 0:
                    return  #msg.wParam
                windll.user32.TranslateMessage(self.pMsg)
                windll.user32.DispatchMessageA(self.pMsg)
            break

        return timeGetTime()

    def end_frame(self):
        ps = PAINTSTRUCT()
        hdc = BeginPaint(self.window.hwnd, byref(ps))
        if hdc:
            SwapBuffers(hdc)
        EndPaint(self.window.hwnd, byref(ps))


def mainloop(controller, **kw):
    loop = LoopManager(controller, **kw)
    lastCount = None
    while True:
        count = loop.begin_frame()
        if not count:
            break
        d = count - lastCount if lastCount else 0
        lastCount = count
        if d > 0:
            controller.onUpdate(d)
            controller.draw()
            loop.end_frame()


if __name__ == "__main__":
    from logging import basicConfig, DEBUG
    basicConfig(format='%(levelname)s:%(name)s:%(message)s', level=DEBUG)
    import os
    if os.name != 'nt':
        logger.debug("this script is windows only: " + os.name)
        sys.exit()
    import glglue.sample
    mainloop(glglue.sample.SampleController(),
             width=600,
             height=400,
             version="3.2")
