from logging import getLogger
logger = getLogger(__name__)
import pathlib
import struct
from OpenGL.GL import *  # pylint: disable=W0614, W0622, W0401
HERE = pathlib.Path(__file__).absolute().parent


VS = '''
#version 330
in vec2 aPosition;
void main ()
{
    gl_Position = vec4(aPosition, 1, 1);
}
'''

FS = '''
#version 330
out vec4 FragColor;
void main()
{
    FragColor = vec4(1, 1, 1, 1);
}
'''


class Controller:
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """
    def __init__(self) -> None:
        self.shader = None
        self.is_initialized = False
        self.vbo = False

    def onResize(self, w: int, h: int) -> None:
        logger.debug('onResize: %d, %d', w, h)
        glViewport(0, 0, w, h)

    def onLeftDown(self, x: int, y: int) -> None:
        pass

    def onLeftUp(self, x: int, y: int) -> None:
        pass

    def onMiddleDown(self, x: int, y: int) -> None:
        pass

    def onMiddleUp(self, x: int, y: int) -> None:
        pass

    def onRightDown(self, x: int, y: int) -> None:
        pass

    def onRightUp(self, x: int, y: int) -> None:
        pass

    def onMotion(self, x: int, y: int) -> None:
        pass

    def onWheel(self, d: int) -> None:
        pass

    def onKeyDown(self, keycode: int) -> None:
        pass

    def onUpdate(self, d: int) -> None:
        '''
        milliseconds
        '''
        #logger.debug('onUpdate: delta %d ms', d)
        pass

    def initialize(self) -> None:
        import glglue.gl3
        self.shader = glglue.gl3.Shader()
        self.shader.compile(VS, FS)

        self.vbo = glglue.gl3.VBO()
        positions = (
            -1.0,
            -1.0,
            1.0,
            -1.0,
            0.0,
            1.0,
        )
        position_bytes = struct.pack('6f', *positions)
        self.vbo.set_vertex_attribute(2, position_bytes)

        self.is_initialized = True

        # vbo

    def draw(self) -> None:
        if not self.is_initialized:
            self.initialize()
        glClearColor(0.0, 0.0, 1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.shader.use()
        self.vbo.set_slot(0)
        self.vbo.draw()

        glFlush()


def main():
    import sys
    import glglue.wgl
    from logging import basicConfig, DEBUG
    basicConfig(format='%(levelname)s:%(name)s:%(message)s', level=DEBUG)
    if len(sys.argv) < 2:
        print('require file name')
        sys.exit(1)
    src = sys.argv[1]

    controller = Controller()
    loop = glglue.wgl.LoopManager(controller,
                                  width=640,
                                  height=480,
                                  title=b"gltf_viewer")

    logger.debug(glglue.get_info())

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


if __name__ == '__main__':
    main()
