from minio import Minio

from L3MinioCache.CacheInterface import L2Cache, L3Cache
from L3MinioCache.MinioL3Cache import MinioL3Cache
from L3MinioCache.PickleL2Cache import PickleL2Cache
from L3MinioCache.FileL2Cache import FileL2Cache
import copy, inspect, hashlib
import logging


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
    def __init__(self,
                 l2: L2Cache = None,  # prefered if your created the caches previously
                 l3: L3Cache = None,  # prefered if your created the caches previously
                 minio_client: Minio = None,
                 local_storage_path: str = 'local_storage',
                 bucket_name: str = None,
                 location: str = "us-east-1"):
        self.l2 = l2
        if l2 is None: self.l2 = PickleL2Cache(local_storage_path)
        self.l3 = l3
        if l3 is None:
            if bucket_name is None or minio_client is None:
                raise Exception('Must define bucket name and minio client')
            self.l3 = MinioL3Cache(minio_client, bucket_name, location)

    def load(self, name: str):
        """Load from l2 or l3 in case of l2 cache miss"""
        result = self.l2.load(name)
        if result is not None:
            logging.debug(f'{name} l2 hit')
            return result
        result = self.l3.load(name)
        if result is not None:
            logging.debug(f'{name} l3 hit')
            self.l2.dump(name, result)
            return result
        logging.debug(f'{name} cache miss')
        return None  # Cache Miss

    def dump(self, name, data):
        """Save in l2 and l3"""
        file_path = self.l2.dump(name, data)
        self.l3.dump(name, file_path)

    def assure_exists(self, name: str):
        """Used to download file from l3 when l2 misses"""
        result = self.l2.exists(name)
        if result:
            logging.debug(f'{name} l2 hit')
            return self.l2.get_path(name)

        self.l3.download(name, self.l2.get_path(name))
        result = self.l2.exists(name)
        if not result:
            raise Exception('file not found anywhere')
        else:
            logging.debug(f'{name} l3 hit')
        return self.l2.get_path(name)
