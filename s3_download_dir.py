import boto3
import os
from tqdm.contrib.concurrent import process_map

S3_SOURCE_DIR = 'fusion-gallery-dataset/consolidated/metadata/'
LOCAL_DEST_DIR = r"D:\FusionGallery\consolidated\metadata/"
BUCKET = '0290-mint-kddw'
# S3_SOURCE_DIR = 'auto3d/manifold1/02691156/'
# LOCAL_DEST_DIR = r"E:\auto3d/manifold1/"
# BUCKET = '0290-mint-grandid'
# S3_SOURCE_DIR = 'ShapeNet/images/9-17/val/'
# LOCAL_DEST_DIR = r"D:\auto3d/validation/"
# BUCKET = 'auto3d-datasets'
S3 = boto3.resource('s3')
BUCKET = S3.Bucket(BUCKET)


def download_s3_file(key):
    target = os.path.join(LOCAL_DEST_DIR, os.path.relpath(key, S3_SOURCE_DIR))
    if not os.path.exists(target):
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        BUCKET.download_file(key, target)
    return


def download_dir_parallel():
    keys = [file.key for file in BUCKET.objects.filter(Prefix=S3_SOURCE_DIR)]
    process_map(download_s3_file, keys, desc='downloading files', max_workers=16, chunksize=1)


if __name__ == '__main__':
    download_dir_parallel()
