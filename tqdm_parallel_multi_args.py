import os
from pathlib import Path
from shutil import copyfile
from tqdm.contrib.concurrent import process_map
from tqdm import tqdm


def get_all_files(directory, pattern):
    return [f for f in tqdm(Path(directory).glob(pattern), f'Getting all files for {pattern}')]


def copy_file_from_list(file, arg1, arg2, arg3):
    # dst = OUT_DIR / file.parts[-3] / file.parts[-2] / file.name
    dst = arg1 / file.parts[-4] / file.parts[-3] / file.suffix
    src = file
    try:
        os.makedirs(dst.parent, exist_ok=True)
        copyfile(src, dst)
    except FileNotFoundError:
        print("FILE NOT FOUND: " + str(file))

    return


def run_worker(args):
    copy_file_from_list(args[0], args[1], args[2], args[3])


def main():
    SRC_DIR = r"D:\FusionGallery\a03\a03.2_png"
    OUT_DIR = Path(r"D:\FusionGallery\a03\a03.2_png_split")

    files = get_all_files(SRC_DIR, '*/*/*.png')

    worker_args = [(file, OUT_DIR, "arg0", "arg1") for file in tqdm(files, desc='generating worker args')]
    process_map(run_worker, worker_args, desc="Copying files", max_workers=16, chunksize=1)


if __name__ == '__main__':
    main()
