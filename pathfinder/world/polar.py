import numpy as np


class PolarWorld:
    def __init__(self, r=1):
        self.__r = r
        self.__t = np.linspace(0, 2 * np.pi, 100)

    def add_to_axes(self, ax):
        ax.plot(np.cos(self.__t), np.sin(self.__t), linewidth=1, color='k')
