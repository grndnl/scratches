import os
from pathlib import Path
from shutil import copyfile
from tqdm import tqdm

# SRC_DIR = r"F:\FusionGallery\assembly\a2\a02_dedup"
# OUT_DIR = Path(r"F:\FusionGallery\assembly\a2\a02_dedup_200_single_png")
# SRC_DIR = r"F:\FusionGallery\assembly\a03_dedup"
# OUT_DIR = Path(r"F:\FusionGallery\assembly\a03_dedup_multiple_png")
# SRC_DIR = r"E:\shpenet excluded"
# OUT_DIR = Path(r"E:\ShapeNetCore.v2.single")
# SRC_DIR = r"F:\FusionGallery\assembly\a3\a03_dedup"
# OUT_DIR = Path(r"F:\FusionGallery\assembly\a3\a03_dedup_json")
# OUT_DIR = Path(r"F:\FusionGallery\assembly\a3\a03_dedup_assembly_png")
SRC_DIR = r"D:\FusionGallery\a1.0.0"
OUT_DIR = Path(r"D:\FusionGallery\a1.0.0_step")


def get_all_files(directory, pattern):
    return [f for f in Path(directory).glob(pattern)]


def copy_files_from_list(file_list, dest_dir):
    count = 0
    for file in tqdm(file_list, desc="Copying files"):
        # dst = OUT_DIR.joinpath(str(file.parts[-2]) + file.suffix)
        dst = OUT_DIR / file.parts[-2] / file.name
        # dst = OUT_DIR / file.parts[-4] / (file.parts[-3] + file.suffix)
        src = file
        try:
            os.makedirs(dst.parent, exist_ok=True)
            if not Path(dst).exists():
                copyfile(src, dst)
                count += 1
        except:
            print("FILE NOT FOUND: " + str(file))

    return count


# files = get_all_files(SRC_DIR, '**/**/*v0.png')
# files = get_all_files(SRC_DIR, '*/**/assembly.png')
# files = get_all_files(SRC_DIR, '*/**/*-*.png')
# files = get_all_files(SRC_DIR, '*/models/*-*.png')
# files = get_all_files(SRC_DIR, '**/**/**/*.obj')
files = get_all_files(SRC_DIR, '*/assembly.json') + get_all_files(SRC_DIR, '*/assembly.step')
# files = get_all_files(SRC_DIR, '*/assembly.png')
# files = get_all_files(SRC_DIR, '*/*.png')
print(f"Copying {len(files)} from {SRC_DIR} to {OUT_DIR}")
# files = files[:1000]
count = copy_files_from_list(files, Path(OUT_DIR))
print(count)

print("Done")
