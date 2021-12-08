from typing import Optional
import sys
from logging import getLogger
from OpenGL import GL
import OpenGL.error
from ctypes import wintypes
import ctypes
from glglue import ctypesmath

from glglue.basecontroller import BaseController
from . import win32con
logger = getLogger(__name__)


##############################################################################
# Windows types
##############################################################################
def ErrorIfZero(handle):
    if handle == 0:
        raise ctypes.WinError()
    else:
        return handle


def LOWORD(n):
    return n & 0xFFFF


def HIWORD(n):
    return (n >> 16) & 0XFFFF


WNDPROC = ctypes.WINFUNCTYPE(
    ctypes.c_int, wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM)


class WNDCLASS(ctypes.Structure):
    _fields_ = [('style', ctypes.c_uint), ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', ctypes.c_int), ('cbWndExtra', ctypes.c_int),
                ('hInstance', wintypes.HANDLE), ('hIcon',
                                                 wintypes.HANDLE), ('hCursor', wintypes.HANDLE),
                ('hbrBackground', wintypes.HANDLE), ('lpszMenuName', wintypes.LPCSTR),
                ('lpszClassName', wintypes.LPCSTR)]


class CREATESTRUCT(ctypes.Structure):
    _fields_ = [('lpCreateParams', ctypes.c_void_p), ('hInstance', wintypes.HANDLE),
                ('hMenu', wintypes.HANDLE), ('hwndParent',
                                             wintypes.HWND), ('cy', ctypes.c_int),
                ('cx', ctypes.c_int), ('y', ctypes.c_int), ('x',
                                                            ctypes.c_int), ('style', ctypes.c_int),
                ('lpszName', wintypes.LPCSTR), ('lpszClass', wintypes.LPCSTR),
                ('dwExStyle', ctypes.c_int)]


class PIXELFORMATDESCRIPTOR(ctypes.Structure):
    _fields_ = [
        ('nSize', ctypes.c_ushort),
        ('nVersion', ctypes.c_ushort),
        ('dwFlags', ctypes.c_ulong),
        ('iPixelType', ctypes.c_ubyte),
        ('cColorBits', ctypes.c_ubyte),
        ('cRedBits', ctypes.c_ubyte),
        ('cRedShift', ctypes.c_ubyte),
        ('cGreenBits', ctypes.c_ubyte),
        ('cGreenShift', ctypes.c_ubyte),
        ('cBlueBits', ctypes.c_ubyte),
        ('cBlueShift', ctypes.c_ubyte),
        ('cAlphaBits', ctypes.c_ubyte),
        ('cAlphaShift', ctypes.c_ubyte),
        ('cAccumBits', ctypes.c_ubyte),
        ('cAccumRedBits', ctypes.c_ubyte),
        ('cAccumGreenBits', ctypes.c_ubyte),
        ('cAccumBlueBits', ctypes.c_ubyte),
        ('cAccumAlphaBits', ctypes.c_ubyte),
        ('cDepthBits', ctypes.c_ubyte),
        ('cStencilBits', ctypes.c_ubyte),
        ('cAuxBuffers', ctypes.c_ubyte),
        ('iLayerType', ctypes.c_ubyte),
        ('bReserved', ctypes.c_ubyte),
        ('dwLayerMask', ctypes.c_ulong),
        ('dwVisibleMask', ctypes.c_ulong),
        ('dwDamageMask', ctypes.c_ulong),
    ]


class RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long), ('top', ctypes.c_long), ('right', ctypes.c_long),
                ('bottom', ctypes.c_long)]


class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [('hdc', wintypes.HDC), ('fErase', wintypes.BOOL), ('rcPaint', RECT),
                ('fRestore', wintypes.BOOL), ('fIncUpdate', wintypes.BOOL),
                ('rgbReserved', ctypes.c_char * 32)]


class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_long), ('y', ctypes.c_long)]


class MSG(ctypes.Structure):
    _fields_ = [('hwnd', wintypes.HWND), ('message', ctypes.c_uint), ('wParam', wintypes.WPARAM),
                ('lParam', wintypes.LPARAM), ('time', ctypes.c_int), ('pt', POINT)]


ShowWindow = ctypes.windll.user32.ShowWindow
ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
ShowWindow.restype = wintypes.BOOL

RegisterClass = ctypes.windll.user32.RegisterClassA
RegisterClass.argtypes = [ctypes.c_void_p]
RegisterClass.restype = wintypes.ATOM

CreateWindowEx = ctypes.windll.user32.CreateWindowExA
CreateWindowEx.argtypes = [
    ctypes.c_int, wintypes.LPCSTR, wintypes.LPCSTR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.HWND, wintypes.HANDLE,
    wintypes.HANDLE, ctypes.py_object
]
CreateWindowEx.restype = wintypes.HWND

if sys.maxsize > 2**32:
    # 64bit
    SetWindowLongPtr = ctypes.windll.user32.SetWindowLongPtrA
    SetWindowLongPtr.argtypes = [wintypes.HWND,
                                 ctypes.c_int, ctypes.c_void_p]
    SetWindowLongPtr.restype = ctypes.c_void_p

    GetWindowLongPtr = ctypes.windll.user32.GetWindowLongPtrA
    GetWindowLongPtr.argtypes = [wintypes.HWND, ctypes.c_int]
    GetWindowLongPtr.restype = ctypes.c_void_p
else:
    # 64bit
    SetWindowLongPtr = ctypes.windll.user32.SetWindowLongA
    SetWindowLongPtr.argtypes = [wintypes.HWND,
                                 ctypes.c_int, ctypes.c_void_p]
    SetWindowLongPtr.restype = ctypes.c_void_p

    GetWindowLongPtr = ctypes.windll.user32.GetWindowLongA
    GetWindowLongPtr.argtypes = [wintypes.HWND, ctypes.c_int]
    GetWindowLongPtr.restype = ctypes.c_void_p

GetDC = ctypes.windll.user32.GetDC
GetDC.argtypes = [wintypes.HWND]

BeginPaint = ctypes.windll.user32.BeginPaint
BeginPaint.argtypes = [wintypes.HWND, ctypes.c_void_p]
BeginPaint.restype = wintypes.HDC

EndPaint = ctypes.windll.user32.EndPaint
EndPaint.argtypes = [wintypes.HWND, ctypes.c_void_p]
EndPaint.restype = wintypes.HDC

ChoosePixelFormat = ctypes.windll.gdi32.ChoosePixelFormat
ChoosePixelFormat.argtypes = [wintypes.HDC, ctypes.c_void_p]
ChoosePixelFormat.restype = ErrorIfZero

SetPixelFormat = ctypes.windll.gdi32.SetPixelFormat
SetPixelFormat.argtypes = [
    wintypes.HDC,
    ctypes.c_int,
    ctypes.c_void_p,
]
SetPixelFormat.restype = ErrorIfZero

SwapBuffers = ctypes.windll.gdi32.SwapBuffers
SwapBuffers.argtypes = [
    wintypes.HDC,
]
SwapBuffers.restype = ErrorIfZero

wglCreateContext = ctypes.windll.opengl32.wglCreateContext
wglCreateContext.argtypes = [
    wintypes.HDC,
]
wglCreateContext.restype = ErrorIfZero

wglDeleteContext = ctypes.windll.opengl32.wglDeleteContext

wglMakeCurrent = ctypes.windll.opengl32.wglMakeCurrent
wglMakeCurrent.argtypes = [
    wintypes.HDC,
    wintypes.HANDLE,
]
wglMakeCurrent.restype = ErrorIfZero

wglGetProcAddress = ctypes.windll.opengl32.wglGetProcAddress
wglGetProcAddress.argtypes = [ctypes.c_void_p]
wglGetProcAddress.restype = ErrorIfZero

DefWindowProc = ctypes.windll.user32.DefWindowProcA
DefWindowProc.argtypes = [wintypes.HWND,
                          ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
DefWindowProc.restype = ctypes.c_int

timeGetTime = ctypes.windll.winmm.timeGetTime
timeGetTime.argtypes = []
timeGetTime.restype = ctypes.c_ulong

##############################################################################
# api class
##############################################################################


class Window(object):
    def __init__(self):
        self.hwnd = None
        self.hrc = None
        self.controller: Optional[BaseController] = None
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
        self.mouse_left = False
        self.mouse_right = False
        self.mouse_middle = False
        self.mouse_capture = False

    def finalize(self):
        logger.debug('finalize %s', self.__class__)

    def update_mouse(self, left, middle, right):
        self.mouse_left = left
        self.mouse_middle = middle
        self.mouse_right = right
        if left or middle or right:
            if not self.mouse_capture:
                ctypes.windll.user32.SetCapture(self.hwnd)
                self.mouse_capture = True
        else:
            if self.mouse_capture:
                ctypes.windll.user32.ReleaseCapture()
                self.mouse_capture = False

    def Redraw(self):
        ctypes.windll.user32.InvalidateRect(
            self.hwnd, ctypes.c_int(0), ctypes.c_int(0))

    def Show(self):
        ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
        ctypes.windll.user32.UpdateWindow(self.hwnd)

    def SetLongPtr(self, hwnd, key, value):
        self.ptrs[key] = value
        SetWindowLongPtr(hwnd, key, value)

    def onPaint(self, hwnd, message, wParam, lParam):
        ps = PAINTSTRUCT()
        hdc = BeginPaint(hwnd, ctypes.byref(ps))
        # if self.hrc and self.controller:
        #     self.controller.draw()
        #     SwapBuffers(hdc)
        EndPaint(hwnd, ctypes.byref(ps))
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
        ctypes.windll.user32.PostQuitMessage(0)
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
        self.update_mouse(False, self.mouse_middle, self.mouse_right)
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onLeftUp(x, y):
                self.Redraw()
        return 0

    def onLeftDown(self, hwnd, message, wParam, lParam):
        self.update_mouse(True, self.mouse_middle, self.mouse_right)
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onLeftDown(x, y):
                self.Redraw()
        return 0

    def onMiddleUp(self, hwnd, message, wParam, lParam):
        self.update_mouse(self.mouse_left, False, self.mouse_right)
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onMiddleUp(x, y):
                self.Redraw()
        return 0

    def onMiddleDown(self, hwnd, message, wParam, lParam):
        self.update_mouse(self.mouse_left, True, self.mouse_right)
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onMiddleDown(x, y):
                self.Redraw()
        return 0

    def onRightUp(self, hwnd, message, wParam, lParam):
        self.update_mouse(self.mouse_left, self.mouse_middle, False)
        if self.controller:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            if self.controller.onRightUp(x, y):
                self.Redraw()
        return 0

    def onRightDown(self, hwnd, message, wParam, lParam):
        self.update_mouse(self.mouse_left, self.mouse_middle, True)
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
        pfd.nsize = ctypes.sizeof(PIXELFORMATDESCRIPTOR)
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

        pixelFormat = ChoosePixelFormat(hdc, ctypes.byref(pfd))
        SetPixelFormat(hdc, pixelFormat, ctypes.byref(pfd))

        self.hrc = wglCreateContext(hdc)
        wglMakeCurrent(hdc, self.hrc)

        if version or profile:
            p = wglGetProcAddress("wglCreateContextAttribsARB".encode('utf-8'))
            if not p:
                raise Exception()
            wglCreateContextAttribsARB = ctypes.WINFUNCTYPE(ctypes.c_void_p, wintypes.HDC, ctypes.c_void_p,
                                                            ctypes.POINTER(ctypes.c_int))(p)

            attribs = []
            if version:
                major, minor = version.split('.')
                attribs.append(win32con.WGL_CONTEXT_MAJOR_VERSION_ARB)
                attribs.append(int(major))
                attribs.append(win32con.WGL_CONTEXT_MINOR_VERSION_ARB)
                attribs.append(int(minor))

            attribs.append(win32con.WGL_CONTEXT_FLAGS_ARB)
            attribs.append(0)

            if profile == 'core':
                attribs.append(win32con.WGL_CONTEXT_PROFILE_MASK_ARB)
                attribs.append(win32con.WGL_CONTEXT_CORE_PROFILE_BIT_ARB)
            elif profile == 'compatibility':
                attribs.append(win32con.WGL_CONTEXT_PROFILE_MASK_ARB)
                attribs.append(
                    win32con.WGL_CONTEXT_COMPATIBILITY_PROFILE_BIT_ARB)

            attribs.append(0)

            array = (ctypes.c_int * len(attribs))(*attribs)
            hrc = wglCreateContextAttribsARB(
                hdc, None, array)
            wglDeleteContext(self.hrc)
            self.hrc = hrc
            wglMakeCurrent(hdc, self.hrc)

        for x in [
                'GL_VERSION',
                # 'GL_EXTENSIONS',
                'GL_SHADING_LANGUAGE_VERSION',
                'GL_RENDERER'
        ]:
            logger.info('%s: %s', x, GL.glGetString(getattr(GL, x)))

        # GL_ARB_compatibility
        profile = None
        try:
            extensions = GL.glGetString(GL.GL_EXTENSIONS).decode(  # type: ignore
                'ascii').split()
            if 'GL_ARB_compatibility' in extensions:
                profile = 'COMPATIBILITY'
        except OpenGL.error.GLerror as ex:
            profile = 'CORE'
        logger.info('OpenGL%d.%d %s', GL.glGetInteger(GL.GL_MAJOR_VERSION),
                    GL.glGetInteger(GL.GL_MINOR_VERSION), profile)

    @staticmethod
    def WndProcProxy(hwnd, message, wParam, lParam):
        # sys.stderr.write("Window::WndProcProxy\n")
        p = GetWindowLongPtr(hwnd, win32con.GWL_USERDATA)
        window = ctypes.cast(p, ctypes.py_object)
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
        wndclass.hInstance = ctypes.windll.kernel32.GetModuleHandleA(
            wintypes.HANDLE(win32con.NULL))
        wndclass.hIcon = ctypes.windll.user32.LoadIconA(
            wintypes.HANDLE(win32con.NULL), wintypes.LPCSTR(win32con.IDI_APPLICATION))
        wndclass.hCursor = ctypes.windll.user32.LoadCursorA(
            wintypes.HANDLE(win32con.NULL), wintypes.LPCSTR(win32con.IDC_ARROW))
        # wndclass.hbrBackground = ctypes.windll.gdi32.GetStockObject(
        #     ctypes.c_int(win32con.WHITE_BRUSH))
        wndclass.hbrBackground = None
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = className
        # Register Window Class
        res = RegisterClass(ctypes.byref(wndclass))
        # logger.debug(res)
        if not res:
            raise ctypes.WinError()
        self.classes.append(wndclass)
        return wndclass

    def create(self, klass,
               width=win32con.CW_USEDEFAULT,
               height=win32con.CW_USEDEFAULT,
               wndclass=None,
               title=b"glglue.wgl",
               ):
        if not wndclass:
            wndclass = self.wndclass

        window = klass()
        pywindow = ctypes.py_object(window)
        hwnd = CreateWindowEx(0, wndclass.lpszClassName, title,
                              win32con.WS_OVERLAPPEDWINDOW,
                              win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                              width, height, win32con.NULL, win32con.NULL,
                              wndclass.hInstance, pywindow)
        self.windows.append(pywindow)
        return window

    def loop(self, window):
        msg = MSG()
        pMsg = ctypes.pointer(msg)
        NULL = ctypes.c_int(win32con.NULL)
        # while ctypes.windll.user32.GetMessageA( pMsg, NULL, 0, 0) != 0:
        #    ctypes.windll.user32.TranslateMessage(pMsg)
        #    ctypes.windll.user32.DispatchMessageA(pMsg)
        lastCount = timeGetTime()
        while True:
            if ctypes.windll.user32.PeekMessageA(pMsg, NULL, 0, 0,
                                                 win32con.PM_NOREMOVE) != 0:
                if ctypes.windll.user32.GetMessageA(pMsg, NULL, 0, 0) == 0:
                    return msg.wParam
                ctypes.windll.user32.TranslateMessage(pMsg)
                ctypes.windll.user32.DispatchMessageA(pMsg)
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
            lpcreatestruct = ctypes.cast(lParam, ctypes.POINTER(CREATESTRUCT))
            createstruct = lpcreatestruct.contents
            window = ctypes.cast(
                createstruct.lpCreateParams, ctypes.py_object).value
            window.hwnd = hwnd
            window.SetLongPtr(hwnd, win32con.GWL_USERDATA,
                              createstruct.lpCreateParams)
            window.SetLongPtr(hwnd, win32con.GWL_WNDPROC,
                              ctypes.cast(WNDPROC(Window.WndProcProxy), ctypes.c_void_p))
            return window.WndProc(hwnd, message, wParam, lParam)

        elif message == win32con.WM_DESTROY:
            ctypes.windll.user32.PostQuitMessage(0)
            return 0

        return DefWindowProc(hwnd, message, wParam, lParam)


class LoopManager:
    def __init__(self, controller: BaseController,
                 width=win32con.CW_USEDEFAULT,
                 height=win32con.CW_USEDEFAULT,
                 wndclass=None,
                 title=b"glglue.wgl",
                 version=None,
                 profile=None,
                 ):
        self.controller = controller
        self.factory = WindowFactory()
        self.window: Window = self.factory.create(
            Window, width=width, height=height, wndclass=wndclass, title=title)
        self.window.createGLContext(16,
                                    version=version,
                                    profile=profile)
        self.window.controller = controller
        ShowWindow(self.window.hwnd, win32con.SW_SHOWNORMAL)
        self.msg = MSG()
        self.pMsg = ctypes.pointer(self.msg)
        self.NULL = ctypes.c_int(win32con.NULL)

    def begin_frame(self):
        while True:
            if ctypes.windll.user32.PeekMessageA(self.pMsg, self.NULL, 0, 0,
                                                 win32con.PM_NOREMOVE) != 0:
                if ctypes.windll.user32.GetMessageA(self.pMsg, self.NULL, 0, 0) == 0:
                    return  # msg.wParam
                ctypes.windll.user32.TranslateMessage(self.pMsg)
                ctypes.windll.user32.DispatchMessageA(self.pMsg)
            break

        return timeGetTime()

    def end_frame(self):
        ps = PAINTSTRUCT()
        hdc = BeginPaint(self.window.hwnd, ctypes.byref(ps))
        if hdc:
            SwapBuffers(hdc)
        EndPaint(self.window.hwnd, ctypes.byref(ps))


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
