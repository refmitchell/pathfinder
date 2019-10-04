# Test file: Anything snippet that is to be kept should be copied to its own file

# Pathfinder imports
from pathfinder.world import *


# Python library imports
from mpl_toolkits.mplot3d import Axes3D  # This seems to be required, though PyCharm disagrees
import matplotlib.pyplot as plt
import matplotlib.colors as cls
import numpy as np


if __name__ == '__main__':
    devax = DevAxes(magnitude=0.5)
    dome = Dome()

    light = Light(Vec3(3, np.pi/4, 0))

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    devax.add_to_world(ax)
    dome.add_to_world(ax)
    light.add_to_world(ax)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    #ax.set_axis_off()
    plt.show()