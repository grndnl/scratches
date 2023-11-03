import os
from pathlib import Path
from tqdm import tqdm


DIR = r"D:\FusionGallery\a03\a03.15_top40_png_split"


def get_all_files(directory, pattern):
    return [f for f in Path(directory).glob(pattern)]


def delete_files(file_list):
    for file in tqdm(file_list, desc="Deleting files"):
        os.remove(file)


files = get_all_files(DIR, "**/*.png")

delete_files(files)
