# Test file: Anything snippet that is to be kept should be copied to its own file

# Pathfinder imports
from pathfinder.world.light import Light
from pathfinder.world.wind import Wind
from pathfinder.world.dome import Dome
from pathfinder.world.devaxes import DevAxes
from pathfinder.world.beetle import Beetle
from pathfinder.definitions import ROOT_DIR, CONFIG_FILE
from pathfinder.util.deserialiser import Deserialiser

# Python library imports
from mpl_toolkits.mplot3d import Axes3D  # This seems to be required, though PyCharm disagrees
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    print("Project root directory: " + ROOT_DIR)
    print("Using configuration file: " + CONFIG_FILE)

    deserialiser = Deserialiser()
    cue_list = deserialiser.get_configuration()

    devax = DevAxes(magnitude=0.5)
    dome = Dome()
    beetle = Beetle()

    entity_list = [dome, beetle]

    cue_list_roll_one = cue_list[0]
    cue_list_roll_two = cue_list[1]

    fig = plt.figure()
    ax = fig.add_subplot(221, projection='3d')
    ax2 = fig.add_subplot(222, projection='3d')

    # Add world entities to both axes
    for x in entity_list:
        x.add_to_world(ax)
        x.add_to_world(ax2)

    for x in cue_list_roll_one:
        x.add_to_world(ax)

    for x in cue_list_roll_two:
        x.add_to_world(ax2)

    '''
    #devax.add_to_world(ax)
    dome.add_to_world(ax)
    light.add_to_world(ax)
    wind.add_to_world(ax)
    beetle.add_to_world(ax)

    dome.add_to_world(ax2)
    light.add_to_world(ax2)
    wind.add_to_world(ax2)
    beetle.add_to_world(ax2)

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
    '''

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.view_init(elev=40, azim=-130)
    ax2.view_init(elev=40, azim=-130)
    ax.set_axis_off()
    ax2.set_axis_off()
    plt.show()
