import matplotlib.pyplot
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from pathlib import Path
import random


def plot_images(image_data, grid_size):
    image_data = [matplotlib.pyplot.imread(image) for image in image_data]
    fig = plt.figure(figsize=(grid_size[1], grid_size[0]))
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                     nrows_ncols=(grid_size[0], grid_size[1]),  # creates 2x2 grid of axes
                     axes_pad=0,  # pad between axes in inch.
                     )

    for ax, im in zip(grid, image_data):
        # Iterating over the grid returns the Axes.
        ax.axis('off')
        ax.imshow(im)

    plt.tight_layout()

    return plt


def get_all_files(directory, pattern):
    return [f for f in Path(directory).glob(pattern)]


def main(input_dir, output_dir, grid_size):
    # files = get_all_files(input_dir, "*/assembly.png")
    files = get_all_files(input_dir, "*.png")
    files = random.sample(files, grid_size[0]*grid_size[1])

    image_grid = plot_images(files, grid_size)

    image_grid.savefig(output_dir + "/assembly-grid.png", bbox_inches='tight', dpi=300)
    image_grid.show()
    return


if __name__ == "__main__":
    # input_dir = r"D:\FusionGallery\a03\a03.2"
    # output_dir = r"D:\FusionGallery\a03"
    input_dir = r"D:\FusionGallery\a03\a03.2_rendering3"
    output_dir = r"D:\FusionGallery\a03"
    grid_size = (15, 12)

    main(input_dir, output_dir, grid_size)
