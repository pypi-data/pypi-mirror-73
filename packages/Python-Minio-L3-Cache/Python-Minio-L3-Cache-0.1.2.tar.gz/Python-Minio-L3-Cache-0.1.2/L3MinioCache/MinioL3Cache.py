from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists, NoSuchKey)

from L3MinioCache.CacheInterface import L3Cache


class MinioL3Cache(L3Cache):
    def __init__(self, minio_client: Minio,
                 bucket_name: str,
                 location: str = "us-east-1"):
        self.minio_client = minio_client
        self.bucket_name = bucket_name
        self.location = location

        if not self.minio_client.bucket_exists(self.bucket_name):
            try:
                self.minio_client.make_bucket(self.bucket_name, location=location)
            except BucketAlreadyOwnedByYou as err:
                pass
            except BucketAlreadyExists as err:
                pass
            except ResponseError as err:
                raise

    def exists(self, name):
        try:
            self.minio_client.get_object(
                bucket_name=self.bucket_name,
                object_name=name)
            return True
        except NoSuchKey:
            return False
        except Exception:
            raise

    def load(self, name: str):
        try:
            return self.minio_client.get_object(
                bucket_name=self.bucket_name,
                object_name=name).read()
        except NoSuchKey:
            return None
        except Exception:
            raise

    def download(self, name: str, path: str):
        try:
            return self.minio_client.fget_object(
                bucket_name=self.bucket_name,
                object_name=name,
                file_path=path)
        except NoSuchKey:
            return None
        except Exception:
            raise

    def dump(self, name: str, local_path: str):
        self.minio_client.fput_object(self.bucket_name, name, local_path)
