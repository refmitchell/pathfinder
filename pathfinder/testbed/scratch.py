# Test file: Anything snippet that is to be kept should be copied to its own file

# Pathfinder imports
from pathfinder.world.light import Light
from pathfinder.world.wind import Wind
from pathfinder.world.dome import Dome
from pathfinder.world.devtools import DevAxes, DevCompassMarkings
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
    devcompass = DevCompassMarkings()
    dome = Dome()
    beetle = Beetle()

    entity_list = [dome, devcompass]

    cue_list_roll_one = cue_list[0]
    cue_list_roll_two = cue_list[1]

    fig = plt.figure()
    first_roll_world_ax = fig.add_subplot(221, projection='3d')
    second_roll_world_ax = fig.add_subplot(222, projection='3d')
    first_roll_polar_ax = fig.add_subplot(223, projection='polar')
    second_roll_polar_ax = fig.add_subplot(224, projection='polar')

    # Add world entities to both axes
    for x in entity_list:
        x.add_to_world(first_roll_world_ax)
        x.add_to_world(second_roll_world_ax)

    for x in cue_list_roll_one:
        x.add_to_world(first_roll_world_ax)

    for x in cue_list_roll_two:
        x.add_to_world(second_roll_world_ax)

    beetle.compute_first_path(cue_list_roll_one)
    beetle.compute_second_path(cue_list_roll_two)
    beetle.add_to_world(first_roll_world_ax)
    beetle.add_to_world(second_roll_world_ax, draw_bearing_change=True)


    print(beetle.get_result_string())
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

    first_roll_world_ax.set_title("Roll 1: 3D World")
    first_roll_world_ax.view_init(elev=40, azim=-130)
    first_roll_world_ax.set_axis_off()

    second_roll_world_ax.set_title("Roll 2: 3D World")
    second_roll_world_ax.view_init(elev=40, azim=-130)
    second_roll_world_ax.set_axis_off()

    first_roll_polar_ax.set_rticks([])
    first_roll_polar_ax.set_thetalim(-np.pi, np.pi)
    first_roll_polar_ax.set_xticks(np.linspace(np.pi, -np.pi, 4, endpoint=False))
    first_roll_polar_ax.set_theta_direction(-1)

    first_roll_polar_ax.grid(False)
    first_roll_polar_ax.set_theta_zero_location("N")

    plt.show()
