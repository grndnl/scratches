from tqdm.contrib.concurrent import process_map  # or thread_map
import time


def _foo(my_number):
    square = my_number * my_number
    time.sleep(0.1)
    return square


if __name__ == '__main__':
    r = process_map(_foo, list(range(0, 30)), max_workers=2)
    print(r)
