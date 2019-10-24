from pathfinder.world.cue import Cue
from pathfinder.util.vec3 import Vec3

import pathfinder.configuration as conf

import numpy as np


class Wind(Cue):
    def __init__(self, name, strength=1, direction=np.pi/2):
        """
        A Cue class to represent wind as a cue. In this case the azimuthal angle defines
        the direction of the wind
        :param strength: The strength of the wind
        :param direction: The angular direction of the wind.
        """
        super().__init__(name, strength=strength, azimuth=direction)

        # Wind's default label position is broken so we override it here.
        label_vector = self.get_world_position().copy()
        x, y, z = label_vector.get_cartesian_as_list()
        z += 1  # Add 1 to the z coordinate of this vector
        label_vector.set_cartesian(x, y, z)
        self.set_label_position(label_vector)

    def add_to_world(self, ax):
        """
        Method to add the wind cue to a 3D world (Axes3D)
        :param ax: The Axes3D which represents the world
        :return: Unused
        """
        super().add_to_world(ax)
        world_vector_list = self.get_world_position().get_cartesian_as_list()
        world_vector_lists = [[x, x] for x in world_vector_list]

        origin = self.origin().get_cartesian_as_list()
        origin = [[x, y] for (x, y) in zip(origin, world_vector_list)]
        origin[2] = list(map(lambda x: x + 1, origin[2]))

        ax.quiver(origin[0],
                  origin[1],
                  origin[2],
                  world_vector_lists[0],
                  world_vector_lists[1],
                  world_vector_lists[2],
                  pivot='tip',
                  arrow_length_ratio=0.1)
