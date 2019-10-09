"""
Class to represent a single light cue, green or UV.
"""

from pathfinder.world.cue import Cue

import numpy as np

class Light(Cue):
    def __init__(self, strength=1, elevation=np.pi/4, azimuth=np.pi/2, colour='green'):
        """
        Create a light-based cue with a given position and strength. Default is a light of strength
        1 at 90 degrees azimuth and 45 degrees elevation.
        :param strength: How powerful the light is
        :param elevation: The elevation at which the light sits on the dome. Radians.
        :param azimuth: The azimuth at which the light sits on the dome (from the x-axis). Radians.
        :param colour: The colour of the light, not currently used.
        """
        super().__init__(strength=strength, elevation=elevation, azimuth=azimuth)
        self.__colour = colour

    def add_to_world(self, ax):
        """
        Method to add the light to a 3D world.
        :param ax: The Axes3D which represent the world
        :return: Unused
        """
        world_vector = self.get_world_position().get_cartesian_as_list()
        world_position = [[x] for x in world_vector]

        # Define markersize proportional to cue strength
        # TODO: Maybe change this policy. Visualisation kind of breaks.
        marker_size = str(super().get_strength() * 10)
        ax.plot(world_position[0],
                world_position[1],
                world_position[2],
                color=self.__colour,
                marker='o',
                markersize=marker_size)
