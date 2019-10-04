"""
Class to represent a single light cue, green or UV.
"""

from pathfinder.world import *
from pathfinder.util import *


class Light(Cue):
    def __init__(self, position=Vec3()):
        """
        Create a light-based cue with a given position and strength. Default is a zero vector with
        :param position:
        """
        super().__init__()
        super().set_position(position)

    def add_to_world(self, ax):
        geometric_vector = super().get_position().get_spherical_as_list()
        world_vector = Vec3(magnitude=1, theta=geometric_vector[1], phi=geometric_vector[2])
        world_position = world_vector.get_cartesian_as_list()
        world_position = [[x] for x in world_position]

        ax.plot(world_position[0], world_position[1], world_position[2], color='green', marker='o', markersize='12')
