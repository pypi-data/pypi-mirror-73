import pickle
from pathlib import Path
import os


class PickleL2Cache:
    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)

    def load(self, name):
        full_path = self.storage_path / str(name + ".pickle")
        if not os.path.isfile(full_path):
            return None
        return pickle.load(open(full_path, 'rb'))

    def dump(self, name, data):
        full_path = self.storage_path / str(name + ".pickle")
        pickle.dump(data, open(full_path, 'wb'))
        return full_path
