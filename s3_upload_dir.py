import boto3
import botocore
from os import walk
from tqdm import tqdm
from pathlib import Path
from tqdm.contrib.concurrent import process_map

BUCKET = '0290-mint-grandid'
S3 = boto3.client('s3')

S3_DEST_DIR = 'fusion-gallery/a03/'
SOURCE_DIR = r"D:\FusionGallery\a03\a03.6_obj_split"


def get_all_files(directory, pattern):
    return [f for f in Path(directory).glob(pattern)]


def key_exists(mykey):
    response = S3.list_objects_v2(Bucket=BUCKET, Prefix=mykey)
    if response:
        for obj in response['Contents']:
            if mykey == obj['Key']:
                return True
    return False


def upload_file(file_dir):
    # file_name = file_dir.name
    # if not key_exists(s3_directory + "/" + file_dir.parts[-3] + "/" + file_name):
    with open(str(file_dir), "rb") as f:
        # dest_dir = S3_DEST_DIR + "/" + file_dir.parts[-2] + "/" + file_name
        dest_dir = Path(S3_DEST_DIR) / file_dir.relative_to(SOURCE_DIR)
        S3.upload_fileobj(f, BUCKET, str(dest_dir).replace("\\", "/"))
    return


# def upload_file(file_dir):
#     file_name = file_dir.name
#     try:
#         s3.head_object(BUCKET, s3_directory + "/" + file_dir.parts[-3] + "/" + file_name)
#     except botocore.exceptions.ClientError as e:
#         print(e)
#         if e.response['Error']['Code'] == "404":
#             print(e)
#             with open(str(file_dir), "rb") as f:
#                 s3.upload_fileobj(f, BUCKET, s3_directory + "/" + file_dir.parts[-3] + "/" + file_name)
#             return
#     finally:
#         return
#

def upload_directory(s3, BUCKET, directory, s3_directory):
    file_names = get_all_files(directory, '*/*/*')
    # file_names = file_names[42000:]
    for file_dir in tqdm(file_names):
        file_name = file_dir.name
        # if not key_exists(s3_directory + "/" + file_dir.parts[-3] + "/" + file_name):
        with open(str(file_dir), "rb") as f:
            s3.upload_fileobj(f, BUCKET, s3_directory + "/" + file_dir.parts[-2] + "/" + file_name)
    return


def upload_dir_parallel(directory):
    file_names = get_all_files(directory, '**/*.*')
    # file_names = file_names[0]
    process_map(upload_file, file_names, desc='uploading files', max_workers=32, chunksize=1)


if __name__ == '__main__':
    # BUCKET = '0290-mint-grandid'
    # s3 = boto3.client('s3')
    # s3_directory = 'shapenet'

    # upload_directory(S3, BUCKET, SOURCE_DIR, S3_DEST_DIR)
    upload_dir_parallel(SOURCE_DIR)
