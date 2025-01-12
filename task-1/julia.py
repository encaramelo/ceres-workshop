from pathlib import Path
from warnings import warn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from PIL import Image

from mandelbrot import *

class Julia:
    """
    Class which generates visualisations of Julia sets.

    Args:
        c_value:
            The value of the complex additive constant in the quadratic map
        centre:
            A complex number representing the coordinates of the centre
            of the image
        extent:
            The linear extent of the image, i.e. the size of each dimension
            in the complex plane
        resolution:
            The number of pixels on each row or column; the total number of
            pixels will be the square of ``resolution``
    """

    def __init__(self,c_value:complex,centre:complex,extent:float,resolution:int) -> None:
        self.grid = complex_grid(centre, extent, resolution)
        self.pixels = np.vectorize(self.get_pixel)(c_value, self.grid)

    @staticmethod
    def get_pixel(c:complex, z0: complex) -> int:
        """
        Computes a single 8-bit pixel.

        Args:
            c: The additive constant
            z0: The initial value for z

        Returns:
            Integer between 0 and 255
        """
        for n, z in zip(range(256), quadratic_map(c, z0)):
            if abs(z) >= 2:break
        return n

    def get_figure(self,cmap:str)->plt.Figure:
        """
        Creates a matplotlib Figure visualising the Mandelbrot set.

        Args:
            cmap:
                The colour map used to colour pixels. For available colours
                see matplotlib documentation on colourmaps
        """
        # TODO: it would be nice if we could fall back on a default value
        # for the colourmap if no cmap argument is provided

        grid_min, grid_max= self.grid.min(),self.grid.max()
        fig, ax = plt.subplots()

        ax.imshow(self.pixels,
            cmap=cmap,
        extent=(grid_min.real,grid_max.real,grid_min.imag,grid_max.imag),
            origin="lower")

        ax.set_title("Julia Set")
        ax.set_xlabel("Real axis")
        ax.set_ylabel("Imaginary axis")
        fig.tight_layout()

        return fig

    def get_image(self, cmap: str) -> Image.Image:
        """
        Creates a PIL (pillow) Image visualising the Mandelbrot set
        """
        cmap = get_cmap(cmap)
        image_array = np.uint8(cmap(self.pixels / 255) * 255)
        return Image.fromarray(image_array)

c_value = complex(0, -1)
centre = complex(0, 0)
extent = 1.0
resolution = 500
cmap = "viridis_r"

julia = Julia(c_value, centre, extent, resolution)
fig = julia.get_figure(cmap)
#plt.show()
