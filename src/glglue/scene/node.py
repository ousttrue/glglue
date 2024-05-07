class Transform:
    pass


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.local_transform = Transform()

    def draw(self):
        pass
