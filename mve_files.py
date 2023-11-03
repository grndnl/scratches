from pathlib import Path
import glob
import os



models_path = r'F:/MechanicalComponents/MCB_A/depth/train'
models = sorted(glob.glob(models_path+'/*/*.png'))

# print(models_path)
# print(models)


# root / <label>  / <train/test> / <item> / <view>.png
for model in models:
    parts = Path(model).parts

    root = Path(parts[0], parts[1], parts[2], parts[3])
    label = parts[5]
    train_test = parts[4]
    item = parts[-1].split("_")[0]
    view = parts[-1].split("_")[-1]

    dest_dir = Path.joinpath(root, label, train_test, item)
    print(dest_dir)
    print()

    dest_dir.mkdir(parents=True, exist_ok=True)
    Path(model).rename(dest_dir.joinpath(view))