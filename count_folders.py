import os
from pathlib import Path

dir = Path(r'F:\AssemblyGraph200b\train-test\depth')


class_num = {}
for test_train in ["train"]:
# for test_train in ["test"]:
# for test_train in ["test", "train"]:
    for Class in os.listdir(dir):
        count = 0
        for folder in os.listdir(dir.joinpath(Class) / test_train):
            # print(folder)
            count += 1

            subfolder_count = 0
            for sub_folder in os.listdir(dir / Class / test_train / folder):
                subfolder_count += 1

            if subfolder_count != 12:
                print(Class)
                print(folder)
                print("DEL: " + str(dir / Class / test_train / folder))
                # Path.rmdir(dir / Class / test_train / folder)         # Comment out to not delete

        print(Class + ' count: ' + str(count))
        class_num[Class] = count