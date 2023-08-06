from L3MinioCache.MinioL3Cache import MinioL3Cache
from L3MinioCache.PickleL2Cache import PickleL2Cache
import copy, inspect, hashlib


def make_hash(o):
    """
    Makes a hash from a dictionary, list, tuple or set to any level, that contains
    only other hashable types (including any lists, tuples, sets, and
    dictionaries).
    https://stackoverflow.com/questions/5884066/hashing-a-dictionary
    """
    if isinstance(o, (set, tuple, list)):
        return hash(tuple([make_hash(e) for e in o]))
    elif not isinstance(o, dict) and o.__class__.__module__ == 'builtins':
        return hash(o)
    elif not isinstance(o, dict):
        return make_hash(o.__dict__)

    new_o = copy.deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = make_hash(v)
    return hash(tuple(frozenset(sorted(new_o.items()))))


class L2L3HashedCache:
    def __init__(self, l2l3cache):
        self.cache = l2l3cache

    def execute(self, name, callback, *args):
        gen_hash = hashlib.md5((inspect.getsource(callback) + str(make_hash(args))).encode()).hexdigest()
        path = '_'.join([name, gen_hash])
        ret = self.cache.load(path)
        if ret is None:
            ret = callback(*args)
            self.cache.dump(path, ret)
        return ret


class L2L3Cache:
    def __init__(self, local_storage_path,
                 minio_client,
                 bucket_name,
                 location="us-east-1"):
        self.l2 = PickleL2Cache(local_storage_path)
        self.l3 = MinioL3Cache(minio_client, bucket_name, location)

    def load(self, name):
        result = self.l2.load(name)
        if result is not None:
            # print(f'{name} l2 hit')
            return result
        result = self.l3.load(name)
        if result is not None:
            # print(f'{name} l3 hit')
            self.l2.dump(name, result)
            return result
        # print(f'{name} cache miss')
        return None  # Cache Miss

    def dump(self, name, data):
        file_path = self.l2.dump(name, data)
        self.l3.dump(name, file_path)
