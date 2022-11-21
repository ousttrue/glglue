def main():
    from glglue.scene.triangle import TriangleScene
    import glglue.glfw

    scene = TriangleScene()

    loop = glglue.glfw.LoopManager(title="glfw sample")
    while True:
        frame = loop.begin_frame()
        if not frame:
            break
        scene.render(frame)
        loop.end_frame()


if __name__ == "__main__":
    main()
