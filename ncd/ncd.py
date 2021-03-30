import tempfile
from bz2 import BZ2File
from contextlib import contextmanager
from os import PathLike, path, unlink
from pathlib import Path
from typing import Callable, Generator

# a function from a pathlike object to its compressed size in bytes
Compressor = Callable[[PathLike], int]


def ncd(x: PathLike,
        y: PathLike,
        c: Compressor) -> float:
    cx = c(x)
    cy = c(y)
    with concat(x, y) as xy:
        cxy = c(xy)
    return (cxy - min(cx, cy)) / max(cx, cy)


def bz2(x: PathLike) -> int:
    size = path.getsize(x)
    with tempfile.TemporaryFile() as tmp:
        with BZ2File(tmp, 'wb') as tgt, open(x, 'rb') as src:
            tgt.write(src.read(size))
        return tmp.tell()  # current cursor pos


@contextmanager
def concat(x: PathLike, y: PathLike) -> Generator[PathLike, None, None]:
    """"Return a path to a file that is the concatenation of files `x` and `y`

    The file is cleaned up after the context is closed.
    """
    tmp = tempfile.NamedTemporaryFile(delete=False)
    for f in x, y:
        for chunk in open(f, 'rb'):
            tmp.write(chunk)
    tmp.close()
    try:
        yield Path(tmp.name)
    finally:
        unlink(tmp.name)
