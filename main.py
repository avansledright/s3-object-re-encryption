import boto3
from botocore.exceptions import ClientError
import json
import sys

# GLOBAL:
s3 = boto3.client("s3", region_name="us-west-2")

# Returns a list of objects with a specified prefix
def get_all_objects(s3_bucket, prefix):
    return_obj = []
    try:
        response = s3.list_objects_v2(
            Bucket=s3_bucket,
            Prefix=prefix
        )
        while True:
            for obj in response.get('Contents', []):
                return_obj.append(obj)
            if 'NextContinuationToken' not in response:
                break
            response = s3.list_objects_v2(
                Bucket=s3_bucket,
                Prefix=prefix,
                ContinuationToken=response['NextContinuationToken']
            )
    except ClientError as e:
        print("Failed to get objects")
        print(e)
    return return_obj

# Checks an object's encryption type
def check_encryption(bucket, key):
    try:
        response = s3.head_object(Bucket=bucket, Key=key)
        return response.get('ServerSideEncryption') == 'AES256'
    except ClientError as e:
        print(f"Failed to retrieve info for {key}")
        print(e)
        return False

# Encrypts object with SSE-S3 if not already
def encrypt_with_sse_s3(bucket, key):
    try:
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': key},
            Key=key,
            ServerSideEncryption='AES256'
        )
        print(f"Encryption changed to SSE-S3 for {key}")
    except ClientError as e:
        print(f"Failed to re-encrypt {key}")
        print(e)

if __name__ == "__main__":
    print("Starting S3 Re-encryption process")
    if len(sys.argv) < 3:
        print("USAGE: python3 main.py <bucket name> <prefix>")
        sys.exit(1)

    # Get all objects
    s3_objects = get_all_objects(sys.argv[1], sys.argv[2])
    total_objects = len(s3_objects)
    print(f"There are {total_objects} objects to check")

    # Check and update their encryption if needed
    counter = 0
    for obj in s3_objects:
        key = obj['Key']
        if not check_encryption(sys.argv[1], key):
            print(f"Object {key} is not encrypted with SSE-S3, updating...")
            encrypt_with_sse_s3(sys.argv[1], key)
            counter += 1

    # Return total list of objects updated
    print(f"Successfully updated encryption for {counter} objects")
