from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists, NoSuchKey)


class MinioL3Cache:
    def __init__(self, minio_client, bucket_name, location="us-east-1"):
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

    def load(self, name):
        try:
            return self.minio_client.get_object(
                bucket_name=self.bucket_name,
                object_name=name).read()
        except NoSuchKey:
            return None
        except Exception:
            raise

    def dump(self, name, local_path):
        self.minio_client.fput_object(self.bucket_name, name, local_path)
