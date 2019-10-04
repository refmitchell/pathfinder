
from pathfinder.world.entity import Entity


import matplotlib.pyplot as plt
import matplotlib.colors as cls
import numpy as np


class Dome(Entity):
    def __init__(self, r=1):
        Entity.__init__(self)
        r = 1
        # Make data
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        self.__x = r * np.outer(np.cos(u), np.sin(v))
        self.__y = r * np.outer(np.sin(u), np.sin(v))
        zss = r * np.outer(np.ones(np.size(u)), np.cos(v))
        zss = [[z if z >= 0 else 0 for z in zs] for zs in zss]  # Remove all negative z
        self.__z = np.array(zss)

    def add_to_world(self, ax):
        """
        Method to draw the world dome correctly onto a given 3D axes object.
        :param ax: The Axes3D object onto which we want to draw this surface.
        :return: Unused
        """
        ax.plot_surface(self.__x, self.__y, self.__z, alpha=0.1)
