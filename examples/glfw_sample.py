# coding: utf-8
"""
pip install glfw
"""


def main():
    from glglue.scene.sample import SampleScene
    import glglue.glfw

    scene = SampleScene()

    loop = glglue.glfw.LoopManager(title="glfw sample")
    while True:
        frame = loop.begin_frame()
        if not frame:
            break
        scene.render(frame)
        loop.end_frame()


if __name__ == "__main__":
    main()
