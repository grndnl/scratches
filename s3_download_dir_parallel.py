import boto3
import os
from concurrent import futures

relative_path = 'auto3d/manifold1/'
bucket_name = '0290-mint-grandid'
s3_object_keys = []  # List of S3 object keys
max_workers = 5

abs_path = os.path.abspath(relative_path)
s3 = boto3.client('s3')


def fetch(key):
    file = f'{abs_path}/{key}'
    os.makedirs(file, exist_ok=True)
    with open(file, 'wb') as data:
        s3.download_fileobj(bucket_name, key, data)
    return file


def fetch_all(keys):
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_key = {executor.submit(fetch, key): key for key in keys}

        print("All URLs submitted.")

        for future in futures.as_completed(future_to_key):

            key = future_to_key[future]
            exception = future.exception()

            if not exception:
                yield key, future.result()
            else:
                yield key, exception


for key, result in fetch_all(S3_OBJECT_KEYS):
    print(f'key: {key}  result: {result}')
