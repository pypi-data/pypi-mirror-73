import pickle
from pathlib import Path
import os

from L3MinioCache.CacheInterface import L2Cache


class FileL2Cache(L2Cache):
    def __init__(self, storage_path: str, binary: bool = False):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.binary = "b" if binary else ""

    def get_path(self, name: str, abs_path: bool = True):
        ret = self.storage_path / name
        if abs_path: ret = os.path.abspath(ret)
        return ret

    def exists(self, name: str):
        return os.path.isfile(self.get_path(name))

    def load(self, name: str):
        full_path = self.get_path(name)
        if not os.path.isfile(full_path):
            return None
        f = open(full_path, "r" + self.binary)
        ret = f.read()
        f.close()
        return ret

    def dump(self, name: str, data: str):
        f = open(self.get_path(name), "w" + self.binary)
        f.write(data)
        f.close()
