"""Loads JSON/binary data from S3 when DATA_SOURCE=s3, otherwise falls back to local disk."""
import json
import os

DATA_SOURCE = os.getenv("DATA_SOURCE", "local")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_DATA_PREFIX = os.getenv("S3_DATA_PREFIX", "data")

_s3_client = None


def _get_client():
    global _s3_client
    if _s3_client is None:
        import boto3
        _s3_client = boto3.client("s3")
    return _s3_client


def _require_bucket():
    if not S3_BUCKET:
        raise RuntimeError("S3_BUCKET must be set when DATA_SOURCE=s3")


def _s3_key(local_path):
    relative = local_path.split("data/", 1)[-1]
    return f"{S3_DATA_PREFIX}/{relative}"


def read_json(local_path):
    if DATA_SOURCE == "s3":
        _require_bucket()
        obj = _get_client().get_object(Bucket=S3_BUCKET, Key=_s3_key(local_path))
        return json.loads(obj["Body"].read())

    with open(local_path, "r") as fp:
        return json.load(fp)


def read_bytes(local_path):
    if DATA_SOURCE == "s3":
        _require_bucket()
        obj = _get_client().get_object(Bucket=S3_BUCKET, Key=_s3_key(local_path))
        return obj["Body"].read()

    with open(local_path, "rb") as fp:
        return fp.read()


def list_files(local_folder, suffix=None):
    if DATA_SOURCE == "s3":
        _require_bucket()
        prefix = _s3_key(local_folder.rstrip("/")) + "/"
        paginator = _get_client().get_paginator("list_objects_v2")
        names = []
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix):
            for item in page.get("Contents", []):
                name = item["Key"].split("/")[-1]
                if name and (not suffix or name.endswith(suffix)):
                    names.append(name)
        return names

    return [
        name for name in os.listdir(local_folder)
        if not suffix or name.endswith(suffix)
    ]
