"""
General usage script
-
Expected usage: user defines a configuration file then runs this script on that file. The user is expected
                to do this through the jupyter notebook.
"""

# Pathfinder imports
from pathfinder.world.dome import Dome
from pathfinder.world.devtools import DevAxes, DevCompassMarkings
from pathfinder.world.beetle import Beetle
from pathfinder.util.legends import *
from pathfinder.util.deserialiser import Deserialiser

import pathfinder.configuration as conf
import pathfinder.definitions as defn

# Python library imports
from mpl_toolkits.mplot3d import Axes3D  # This seems to be required, though PyCharm disagrees
import matplotlib.pyplot as plt
import numpy as np
import os


def main(config_file=""):
    # If a config file is specified,
    if config_file != "":
        defn.CONFIG_FILE = os.path.join(defn.CONFIG_DIR, config_file)

    # DEBUG #
    #print("Project root directory: " + defn.ROOT_DIR)
    #print("Using configuration file: " + defn.CONFIG_FILE)

    deserialiser = Deserialiser(configuration_path=defn.CONFIG_FILE)

    deserialiser.init_configuration()

    devcompass = DevCompassMarkings()
    dome = Dome()
    beetle = Beetle()

    entity_list = [dome, devcompass]

    # Get roll configuration from conf module
    cue_list_roll_one = conf.cues_roll_one
    cue_list_roll_two = conf.cues_roll_two

    plt.close('all')
    fig = plt.figure()

    # 3D world axes
    first_roll_world_ax = fig.add_subplot(221, projection='3d')
    second_roll_world_ax = fig.add_subplot(222, projection='3d')

    # Polar axes
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

    # Get the beetle's behaviour
    beetle.compute_first_path(cue_list_roll_one)
    beetle.compute_second_path(cue_list_roll_two)
    beetle.add_to_world(first_roll_world_ax)
    beetle.add_to_world(second_roll_world_ax, draw_bearing_change=True)

    beetle.add_to_polar(first_roll_polar_ax)
    beetle.add_to_polar(second_roll_polar_ax, draw_bearing_change=True)

    # DEBUG #
    # print(beetle.get_result_string())

    # Plot the 3D world for the first roll
    first_roll_world_ax.set_title("Roll 1: 3D World")
    first_roll_world_ax.view_init(elev=40, azim=-130)
    first_roll_world_ax.set_axis_off()


    # Plot the 3D world for the second roll
    second_roll_world_ax.set_title("Roll 2: 3D World")
    second_roll_world_ax.view_init(elev=40, azim=-130)
    second_roll_world_ax.set_axis_off()


    # Polar plot configuration
    first_roll_polar_ax.set_rticks([])
    first_roll_polar_ax.set_rmin(0)
    first_roll_polar_ax.set_rmax(1)
    first_roll_polar_ax.set_thetalim(-np.pi, np.pi)
    first_roll_polar_ax.set_xticks(np.linspace(np.pi, -np.pi, 4, endpoint=False))
    first_roll_polar_ax.grid(False)
    first_roll_polar_ax.set_theta_direction(-1)
    first_roll_polar_ax.set_theta_zero_location("N")
    first_roll_polar_ax.set_title("Roll 1: path and cue vector")

    second_roll_polar_ax.set_rticks([])
    second_roll_polar_ax.set_rmin(0)
    second_roll_polar_ax.set_rmax(1)
    second_roll_polar_ax.set_thetalim(-np.pi, np.pi)
    second_roll_polar_ax.set_xticks(np.linspace(np.pi, -np.pi, 4, endpoint=False))
    second_roll_polar_ax.grid(False)
    second_roll_polar_ax.set_theta_direction(-1)
    second_roll_polar_ax.set_theta_zero_location("N")
    second_roll_polar_ax.set_title("Roll 2: path and cue vector")

    if conf.display_legend:
        # Add legends if they're enabled.
        second_roll_world_ax.legend(handles=create_world_legend_handles(), bbox_to_anchor=(1.05, 1))
        second_roll_polar_ax.legend(handles=create_polar_legend_handles(), bbox_to_anchor=(1.6, 0.2))

    plt.show()

    # Print terminal output: this was modified to make the output more readable. Debug statements are still
    # available as comments.
    print("Project root directory: " + defn.ROOT_DIR)
    print("Using configuration file: " + defn.CONFIG_FILE)
    conf.print_configuration()
    print(beetle.get_result_string())



def wind_and_light_main(cue_info_dictionary):
    """
    Dedicated main for the simplified wind and light case for immediate experiments.
    This will create a configuration file from information provided externally (through a jupyter
    notebook) and then run the software using that configuration.
    :param cue_info_dictionary: Dictionary defining the configuration
    :return: Unused
    """
    from pathfinder.util.serialiser import Serialiser
    filename = "jupyter_auto_conf.yaml"
    Serialiser.write_configuration_dictionary_to_file(cue_info_dictionary, filename)
    main(filename)


if __name__ == '__main__':
    # Note to developer: correct the input file to config.yaml after development; noticed a habit of
    # leaving it as untracked_config which is, well, untracked so people cloning the repo won't have it!
    # TODO: It would be good if this could be set dynamically without needing to change names each time. May be an easy
    # TODO: way to do this by using environment variables or similar.
    main("untracked_config.yaml")



