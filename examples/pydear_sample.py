from typing import Iterable, Dict, Optional, List
import logging
import pathlib
import ctypes
#
import glglue.glfw
from glglue.gl3.pydearcontroller import PydearController
from glglue.gl3.renderview import RenderView
from glglue.windowconfig import WindowConfig
import pydear as ImGui
from pydear.utils.dockspace import DockView
from glglue.scene.node import Node
from glglue.ctypesmath import TRS, Mat4, Camera

logger = logging.getLogger(__name__)

CONFIG_FILE = pathlib.Path("window.ini")


class SceneTree:
    def __init__(self, root: Node) -> None:
        self.root = root
        self.selected = None

    def traverse(self, node: Node):
        flag = ImGui.ImGuiTreeNodeFlags_.OpenOnArrow | ImGui.ImGuiTreeNodeFlags_.OpenOnDoubleClick | ImGui.ImGuiTreeNodeFlags_.SpanAvailWidth
        if not node.children:
            flag |= ImGui.ImGuiTreeNodeFlags_.Leaf
            flag |= ImGui.ImGuiTreeNodeFlags_.Bullet
        if node == self.selected:
            flag |= ImGui.ImGuiTreeNodeFlags_.Selected
        open = ImGui.TreeNodeEx(node.name, flag)
        if ImGui.IsItemClicked():
            # update selectable
            logger.debug(f'select: {node.name}')
            self.selected = node
        if open:
            for child in node.children:
                self.traverse(child)
            ImGui.TreePop()

    def draw(self, p_open: ctypes.Array):
        if ImGui.Begin(self.root.name, p_open):
            self.traverse(self.root)
        ImGui.End()

        # update scene
        self.root.calc_world()


class NodeProp:
    def __init__(self, get_selected, camera: Camera) -> None:
        self.get_selected = get_selected

        # ImGuizmo
        self.camera = camera
        self.matrixTranslation = (ctypes.c_float*3)()
        self.matrixRotation = (ctypes.c_float*3)()
        self.matrixScale = (ctypes.c_float*3)()
        self.mCurrentGizmoOperation = ImGui.OPERATION.ROTATE
        self.mCurrentGizmoMode = ImGui.MODE.WORLD
        self.useSnap = False

    def draw(self, p_open: ctypes.Array):
        if ImGui.Begin('selected node', p_open):
            node: Node = self.get_selected()
            if node:
                ImGui.TextUnformatted(node.name)
                self.edit_transform(node.local_transform)
                # match node.local_transform:
                #     case TRS(t, r, s):
                #         ImGui.SliderFloat3(b'T', t, -10, 10)
                #         ImGui.SliderFloat4(b'R', r, -1, 1)
                #         ImGui.SliderFloat3(b'S', s, -10, 10)
                #     case Mat4() as m:
                #         a = ctypes.addressof(m)
                #         p = ctypes.c_void_p(a)
                #         ImGui.ImGuizmo_DecomposeMatrixToComponents(
                #             p, self.matrixTranslation, self.matrixRotation, self.matrixScale)
                #         ImGui.InputFloat3(b"Tr", self.matrixTranslation)
                #         ImGui.InputFloat3(b"Rt", self.matrixRotation)
                #         ImGui.InputFloat3(b"Sc", self.matrixScale)
                #         ImGui.ImGuizmo_RecomposeMatrixFromComponents(
                #             self.matrixTranslation, self.matrixRotation, self.matrixScale, p)
        ImGui.End()

    def edit_transform(self, m: Mat4):
        ImGui.ImGuizmo_BeginFrame()
        ImGui.ImGuizmo_SetDrawlist()

        # if (ImGui.IsKeyPressed(90))
        #     mCurrentGizmoOperation = ImGui.OPERATION.TRANSLATE
        # if (ImGui.IsKeyPressed(69))
        #     mCurrentGizmoOperation = ImGui.OPERATION.ROTATE
        # if (ImGui.IsKeyPressed(82)) // r Key
        #     mCurrentGizmoOperation = ImGui.OPERATION.SCALE

        if ImGui.RadioButton("Translate", self.mCurrentGizmoOperation == ImGui.OPERATION.TRANSLATE):
            self.mCurrentGizmoOperation = ImGui.OPERATION.TRANSLATE
        ImGui.SameLine()
        if ImGui.RadioButton("Rotate", self.mCurrentGizmoOperation == ImGui.OPERATION.ROTATE):
            self.mCurrentGizmoOperation = ImGui.OPERATION.ROTATE
        ImGui.SameLine()
        if ImGui.RadioButton("Scale", self.mCurrentGizmoOperation == ImGui.OPERATION.SCALE):
            self.mCurrentGizmoOperation = ImGui.OPERATION.SCALE

        ImGui.ImGuizmo_DecomposeMatrixToComponents(
            m, self.matrixTranslation, self.matrixRotation, self.matrixScale)
        ImGui.InputFloat3("Tr", self.matrixTranslation, 3)
        ImGui.InputFloat3("Rt", self.matrixRotation, 3)
        ImGui.InputFloat3("Sc", self.matrixScale, 3)
        ImGui.ImGuizmo_RecomposeMatrixFromComponents(
            self.matrixTranslation, self.matrixRotation, self.matrixScale, m)

        if self.mCurrentGizmoOperation != ImGui.OPERATION.SCALE:
            if ImGui.RadioButton("Local", self.mCurrentGizmoMode == ImGui.MODE.LOCAL):
                self.mCurrentGizmoMode = ImGui.MODE.LOCAL
            ImGui.SameLine()
            if ImGui.RadioButton("World", self.mCurrentGizmoMode == ImGui.MODE.WORLD):
                self.mCurrentGizmoMode = ImGui.MODE.WORLD

        # if (ImGui.IsKeyPressed(83))
        #     useSnap = !useSnap
        # ImGui.Checkbox("", &useSnap)
        # ImGui.SameLine()
        # vec_t snap
        # switch (mCurrentGizmoOperation)
        # {
        # case ImGui.OPERATION.TRANSLATE:
        #     snap = config.mSnapTranslation
        #     ImGui.InputFloat3("Snap", &snap.x)
        #     break
        # case ImGui.OPERATION.ROTATE:
        #     snap = config.mSnapRotation
        #     ImGui.InputFloat("Angle Snap", &snap.x)
        #     break
        # case ImGui.OPERATION.SCALE:
        #     snap = config.mSnapScale
        #     ImGui.InputFloat("Scale Snap", &snap.x)
        #     break
        # }

        io = ImGui.GetIO()
        # x, y = ImGui.GetWindowPos()
        # w, h = ImGui.GetWindowSize()
        # ImGui.ImGuizmo_SetRect(x, y, w, h)
        ImGui.ImGuizmo_SetRect(0, 0, io.DisplaySize.x, io.DisplaySize.y)
        ImGui.ImGuizmo_Manipulate(self.camera.view.matrix, self.camera.projection.matrix, self.mCurrentGizmoOperation, self.mCurrentGizmoMode, m, None, None)#self.useSnap ? &snap.x : NULL)


def cube():
    view = RenderView()
    return [DockView(
        'cube', (ctypes.c_bool * 1)(True), view.draw)]


def teapot():
    view = RenderView()
    from glglue.scene.teapot import create_teapot
    view.scene.drawables = [create_teapot()]
    return [DockView(
        'teapot', (ctypes.c_bool * 1)(True), view.draw)]


def skin():
    view = RenderView()
    from glglue.scene.skin_sample import create_skin

    root = create_skin()
    view.scene.drawables = [root]

    tree = SceneTree(root)
    # prop = NodeProp(lambda: tree.selected, view.camera)

    return [
        DockView('skin', (ctypes.c_bool * 1)(True), view.draw),
        DockView('skin_herarchy', (ctypes.c_bool * 1)(True), tree.draw),
        # DockView('skin_node_prop', (ctypes.c_bool * 1)(True), prop.draw),
    ]


SCENES = {
    'cube': cube,
    'teapot': teapot,
    'skin': skin,
}


class ImguiDocks:
    def __init__(self) -> None:
        self.demo = DockView(
            'demo', (ctypes.c_bool * 1)(True), ImGui.ShowDemoWindow)
        self.metrics = DockView(
            'metrics', (ctypes.c_bool * 1)(True), ImGui.ShowMetricsWindow)
        self.selected = 'skin'
        self.scenes: Dict[str, List[DockView]] = {
            k: [] for k, v in SCENES.items()}

        def show_selector(p_open: ctypes.Array):
            # open new window context
            if ImGui.Begin("SceneSelector", p_open):
                for k, v in self.scenes.items():
                    if ImGui.Selectable(k, k == self.selected):
                        self.selected = k
                # draw text label inside of current window
                if ImGui.Button("Debug"):
                    logger.debug("debug message")
            # close current window context
            ImGui.End()
        self.hello = DockView(
            'hello', (ctypes.c_bool * 1)(True), show_selector)

        # logger
        from pydear.utils.loghandler import ImGuiLogHandler
        log_handle = ImGuiLogHandler()
        log_handle.register_root()
        self.logger = DockView('log', (ctypes.c_bool * 1)
                               (True), log_handle.draw)

    def get_or_create(self, key: str) -> Iterable[DockView]:
        value = self.scenes.get(key)
        if value:
            return value

        # create RenderView
        logger.info(f"create: {key}")
        value = SCENES[key]()
        self.scenes[key] = value
        return value

    def __iter__(self) -> Iterable[DockView]:
        yield self.demo
        yield self.metrics
        yield self.hello
        for dock in self.get_or_create(self.selected):
            yield dock
        yield self.logger


class SampleController(PydearController):
    def imgui_create_docks(self):
        return ImguiDocks()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

    # ImGui
    controller = SampleController()

    # glfw
    loop = glglue.glfw.LoopManager(
        controller,
        config=WindowConfig.load_json_from_path(CONFIG_FILE),
        title="pydear")

    # main loop
    lastCount = 0
    while True:
        count = loop.begin_frame()
        if not count:
            break
        d = count - lastCount
        lastCount = count
        if d > 0:
            controller.onUpdate(d)
            controller.draw()
            loop.end_frame()

    # save window config
    config = loop.get_config()
    config.save_json_to_path(CONFIG_FILE)
