from typing import NamedTuple, Optional
import pathlib


class WindowConfig(NamedTuple):
    x: int
    y: int
    width: int
    height: int
    is_maximized: bool

    @staticmethod
    def load_json_from_path(file: pathlib.Path) -> Optional['WindowConfig']:
        if file.exists():
            import json
            return WindowConfig(**json.loads(file.read_bytes()))

    def save_json_to_path(self, file: pathlib.Path):
        with file.open('w') as w:
            import json
            json.dump(self._asdict(), w)
