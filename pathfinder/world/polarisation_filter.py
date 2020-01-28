"""
Class to represent the bi-directional cue offered by a linear polarising filter.
"""

from pathfinder.world.cue import Cue

import numpy as np
import pathfinder.configuration as conf


class PolarisationFilter(Cue):
    def __init__(self, name, strength=1, azimuth=np.pi/2):
        """
        Create a cue reminiscent of a linear polarising filter, bidirectional (axial) from
        azimuth to azimuth + np.pi.
        :param name: The unique identifying name of the cue.
        :param strength: The strength.
        :param azimuth: The direction of the polarisation cue.
        """
        # Create a "master" cue which is as defined
        # Create a "secondary" cue which is tied and always points in the opposite direction.
        super().__init__(name, strength=strength, azimuth=azimuth)
        self.set_scale_factor(conf.polarisation_multiplier)

        label_vector = self.get_world_position().copy()
        x, y, z = label_vector.get_cartesian_as_list()
        z += 0.9  # Add 1 to the z coordinate of this vector
        label_vector.set_cartesian(x, y, z)
        self.set_label_position(label_vector)
        self.set_scale_factor(conf.polarisation_multiplier)

        # Augment the name so we retain uniqueness
        secondary_name = ""
        self.__secondary_cue = PolarisationFilterMirror(secondary_name, strength=strength, azimuth=(azimuth+np.pi))

    def get_secondary_cue(self):
        return self.__secondary_cue

    def add_to_world(self, ax):
        """
        Add the polarisation cue to the 3D world
        :param ax: The Axes3D object
        :return: Unused
        """
        super().add_to_world(ax)
        colour = 'darkviolet'
        world_vector_list = self.get_world_position().get_cartesian_as_list()
        world_vector_lists = [[x] for x in world_vector_list]

        origin = self.origin().get_cartesian_as_list()
        origin = [[x] for x in origin]

        origin[2] = list(map(lambda x: x + 0.9, origin[2]))

        ax.quiver(origin[0],
                  origin[1],
                  origin[2],
                  world_vector_lists[0],
                  world_vector_lists[1],
                  world_vector_lists[2],
                  arrow_length_ratio=0.1,
                  color=colour)

        self.__secondary_cue.add_to_world(ax)


class PolarisationFilterMirror(Cue):
    def __init__(self, name, strength=1, azimuth=np.pi/2):
        """
        Create the mirrored part of the polarisation filter.
        :param name: The unique identifying name of the cue.
        :param strength: The strength.
        :param azimuth: The direction of the polarisation cue.
        """
        # Create the mirrored cue
        super().__init__(name, strength=strength, azimuth=azimuth)
        self.set_scale_factor(conf.polarisation_multiplier)

    def add_to_world(self, ax):
        """
        Add the polarisation cue to the 3D world
        :param ax: The Axes3D object
        :return: Unused
        """
        super().add_to_world(ax)
        colour = 'darkviolet'
        world_vector_list = self.get_world_position().get_cartesian_as_list()
        world_vector_lists = [[x] for x in world_vector_list]

        origin = self.origin().get_cartesian_as_list()
        origin = [[x] for x in origin]
        origin[2] = list(map(lambda x: x + 0.9, origin[2]))

        ax.quiver(origin[0],
                  origin[1],
                  origin[2],
                  world_vector_lists[0],
                  world_vector_lists[1],
                  world_vector_lists[2],
                  arrow_length_ratio=0.1,
                  color=colour)
