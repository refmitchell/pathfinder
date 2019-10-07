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

    light = Light(strength=5, colour='orange')
    wind = Wind()

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    #devax.add_to_world(ax)
    dome.add_to_world(ax)
    light.add_to_world(ax)
    wind.add_to_world(ax)

    light_vec_list = light.get_vector_description().get_cartesian_as_list()
    wind_vec_list = wind.get_vector_description().get_cartesian_as_list()

    cue_vectors = [[x1, x2] for (x1, x2) in zip(light_vec_list, wind_vec_list)]
    origins = [[x1, x2] for (x1, x2) in [(0,0),(0,0),(0,0)]]

    ax.quiver(origins[0],
              origins[1],
              origins[2],
              cue_vectors[0],
              cue_vectors[1],
              cue_vectors[2],
              color='r',
              arrow_length_ratio=0.1)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    ax.set_axis_off()
    plt.show()