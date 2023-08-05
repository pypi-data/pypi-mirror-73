from secrets import token_bytes
from datetime import timedelta
from base64 import b32encode
from os.path import expanduser, join, isfile
import boto3
import sys

def run():
    uuid = b32encode(token_bytes(16)).decode("utf-8").strip("=")
    config_f = join(expanduser("~"), ".lonny_aws_bin")
    data = sys.stdin.read().encode("utf-8")

    session = boto3.session.Session()
    client = boto3.client("s3")

    if not isfile(config_f):
        suffix = b32encode(token_bytes(16)).decode("utf-8").strip("=").lower()
        bucket_name = f"lonny-aws-bin-{suffix}"
        client.create_bucket(
            Bucket = bucket_name,
            ACL = "public-read",
            CreateBucketConfiguration = dict(
                LocationConstraint = session.region_name
            )
        )
        with open(config_f, "w") as f:
            f.write(bucket_name)

    with open(config_f) as f:
        bucket_name = f.read()

    client.put_object(
        Bucket = bucket_name,
        ACL = "public-read",
        Body = data,
        Key = uuid,
        ContentType = "text/plain"
    )

    object_url = f"https://{bucket_name}.s3.amazonaws.com/{uuid}"
    print(object_url)