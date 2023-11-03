import os
from pathlib import Path
from shutil import copyfile
from tqdm.contrib.concurrent import process_map

# SRC_DIR = r"E:\ShapeNetCore.v2"
# OUT_DIR = Path(r"E:\ShapeNetCore.v2.single2")
SRC_DIR = r"E:\shpenet excluded"
OUT_DIR = Path(r"E:\ShapeNetCore.v2.single2")


def get_all_files(directory, pattern):
    return [f for f in Path(directory).glob(pattern)]


def copy_files_from_list(file):
    # dst = OUT_DIR / file.parts[-3] / file.parts[-2] / file.name
    dst = OUT_DIR / file.parts[-4] / file.parts[-3] / file.suffix
    src = file
    try:
        os.makedirs(dst.parent, exist_ok=True)
        copyfile(src, dst)
    except FileNotFoundError:
        print("FILE NOT FOUND: " + str(file))

    return


# files = get_all_files(SRC_DIR, '**/**/*v0.png')
files = get_all_files(SRC_DIR, '**/**/**/*.obj')
print(len(files))
count = process_map(copy_files_from_list, files, desc="Copying files", max_workers=4, chunksize=1)
print(count)

print("Done")
