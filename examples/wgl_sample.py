# coding: utf-8
"""
Win32APIでOpenGLホストするサンプル。

* Windows専用
* 追加のインストールは不要
"""
import logging

LOGGER = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(message)s", level=logging.DEBUG
    )

    from glglue.scene.triangle import TriangleScene
    import glglue.wgl

    scene = TriangleScene()

    loop = glglue.wgl.LoopManager(width=640, height=480, title=b"sample")

    while True:
        frame = loop.begin_frame()
        if not frame:
            break
        scene.render(frame)
        loop.end_frame()


if __name__ == "__main__":
    main()
