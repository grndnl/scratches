import os
import json
from pathlib import Path


def JSON_concat():

    # open 'r1_m1_d2\\e2_m1_d2_DEPTH.json' as e
    # open 'r1_m1_d2_file_paths.json' as r

    with open('e2_m1_d2_DEPTH.json') as e, open('r1_m1_d2_file_paths.json') as r:
        print('Reading embeddings...')
        e_data = json.load(e)
        print('Reading results...')
        r_data = json.load(r)


        # for each item in r: append the r.predicted to the correct e item
        for item in r_data:
            if item['augmented']:
                item_path = Path(item['file']).parts[-3:]
                # next(it for it in e_data if it[Path(it['file']).parts[-1]] == item_path[-1])
                # next(it for it in e_data if Path(it['file']).parts[-1] == Path(r_data[5]['file']).parts[-1])
                for element in e_data:
                    if (Path(element['file']).parts[-1]) == item_path[-1]:
                        element['predicted'] = item['predicted']


        # Save out the json data

        print()
        print('Saving JSON data...')
        with open('e2_m1_d2_DEPTH_predicted.json', 'w') as f:
            json.dump(e_data, f)
        print('JSON saved')




def main():
    JSON_concat()


if __name__ == '__main__':
    main()