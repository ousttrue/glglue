from typing import Any
import sys
import io
import inspect
import pathlib
import logging
from OpenGL import GL


LOGGER = logging.getLogger(__name__)


def _write_function(w: io.TextIOBase, name: str, f: Any):
    doc = ""
    if f.__doc__:
        doc = f.__doc__.strip()
    sig = inspect.signature(f)
    w.write(
        f"""
def {name}()->None:
    ...
    '''
    {sig}
    {doc}
    '''
"""
    )


def main(out_dir: pathlib.Path):
    pyi = out_dir / "OpenGL/GL.pyi"
    pyi.parent.mkdir(exist_ok=True, parents=True)
    with pyi.open("w", encoding="utf-8") as w:
        w.write(
            f"""
"""
        )
        for k, v in inspect.getmembers(GL):
            if k.startswith("__"):
                continue
            if inspect.ismodule(v):
                continue
            if isinstance(v, GL.constant.IntConstant):
                w.write(f"{k}: int = ...\n")
            if callable(v):
                continue

            # print(k, type(v), v)

        for k, v in inspect.getmembers(GL, callable):
            if inspect.isclass(v):
                continue
            if inspect.isbuiltin(v):
                continue
            _write_function(w, k, v)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"usage: {sys.argv[0]} STUB_DIR")
        sys.exit()

    main(pathlib.Path(sys.argv[1]))
