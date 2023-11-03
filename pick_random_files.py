import os
import random
from pathlib import Path
import shutil

# TOT_AMOUNT = 410
# SRC_DIR = Path("C:\\data\\cfd_dataset\\CFD_Dataset\\train\\fusion")
# DST_DIR = Path("C:\\data\\cfd_expeirment\\train\\fusion_subset")

TOT_AMOUNT = 10
SRC_DIR = Path("C:\\data\\cfd_dataset\\CFD_Dataset\\train\\fusion")
DST_DIR = Path("C:\\data\\cfd_expeirment\\1_augmented\\train\\fusion_subset")


all_classes_files = os.listdir(SRC_DIR)

for i in range(TOT_AMOUNT):
    # copy random file
    file = random.choice(all_classes_files)
    src = SRC_DIR.joinpath(file)

    print('source:      ' + str(src))
    print('destination: ' + str(DST_DIR / file))

    # if not DST_DIR.exists():
    #     os.makedirs(DST_DIR)
    shutil.copy(src, DST_DIR.joinpath(file))

    # delete folder from folders
    all_classes_files.remove(file)