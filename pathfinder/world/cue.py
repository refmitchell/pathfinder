"""
Superclass defining all basic properties for all cues.
All cues have a position (as a Vec3) and a strength.

Default for a cue is placed at the origin with no strength.

Cue is essentially a special case of entity which has additional properties.
"""

from pathfinder.world.entity import Entity
from pathfinder.util.vec3 import Vec3

import pathfinder.configuration as conf

import numpy as np


class Cue(Entity):
    #
    # Ctor.
    #
    def __init__(self, name, strength=1, elevation=0, azimuth=0):
        """
        A superclass to define a generic cue. All cues have strength, elevation, and
        azimuth.
        :param strength: How powerful the cue is
        :param elevation: The elevation at which the cue sits on the dome. Radians.
        :param azimuth: The azimuth at which the cue sits on the dome (from the x-axis). Radians.
        """
        super().__init__()
        self.__strength = strength
        self.__elevation = elevation
        self.__azimuth = azimuth
        self.__world_position = self.__update_world_position()
        self.__name = name

    #
    # Private methods
    #
    def __update_world_position(self):
        """
        Internal helper method to update the underlying vector for this cue. World position
        vectors always have a magnitude of 1. Strength is kept separate.
        :return: The updated vector representation
        """
        _phi = -self.__azimuth
        _theta = (np.pi / 2) - self.__elevation
        return Vec3(magnitude=1, theta=_theta, phi=_phi)



    #
    # Public methods
    # Setters
    #
    def set_position(self, elevation, azimuth):
        """
        Set position using the conventional elevation and azimuth parameters from the Dung beetle
        literature.
        :param elevation: Angle up from the x-axis
        :param azimuth: Azimuthal angle from the x-axis, positive is clockwise, negative is counter-clockwise
        :return: Unused
        """
        self.__elevation = elevation
        self.__azimuth = azimuth
        self.__world_position = self.__update_world_position()

    def set_azimuth(self, azimuth):
        """
        Update only the azimuthal angle of the cue.
        :param azimuth: Azimuthal angle from the x-axis, positive is clockwise, negative is counter-clockwise
        :return: Unused
        """
        self.__azimuth = azimuth
        self.__world_position = self.__update_world_position()

    def set_elevation(self, elevation):
        """
        Update only the elevation angle of the cue.
        :param elevation: Elevation angle up from the x-axis, maximum is pi/2
        :return:
        """
        self.__elevation = elevation
        self.__world_position = self.__update_world_position()

    def set_strength(self, strength):
        self.__strength = strength

    #
    # Getters
    #
    def get_elevation(self):
        return self.__elevation

    def get_azimuth(self):
        return self.__azimuth

    def get_world_position(self):
        """
        Retrieve the world position of the cue.
        :return: The Vec3 object representing where the cue should be located in the world.
        """
        return self.__world_position

    def get_strength(self):
        return self.__strength

    def get_vector_description(self):
        """
        Retrieve the internal geometric description for computation
        :return: A vector with the same direction as the world representation but
        with updated strength.
        """
        world_vector = self.get_world_position()
        world_vector_list = world_vector.get_spherical_as_list()

        # Define a new vector with the updated radius parameter and the same angular position
        return Vec3(magnitude=self.__strength, theta=world_vector_list[1], phi=world_vector_list[2])

    #
    # Optional additions
    #
    def add_optional_elements(self, ax):
        """
        Check the configuration switches and add the desired output to the world.
        :param ax:
        :return: Unused
        """
        if conf.show_labels:
            self.add_label_to_world(ax)
        if conf.show_individual:
            print("debug: individual directions enabled")
        if conf.show_geometry:
            print("debug: geometry enabled")

    def add_label_to_world(self, ax):
        """
        Adds the cue label to the world
        :param ax: The Axes3D object which holds the world
        :return: Unused
        """
        label_str = self.__name

        # Generate label position
        world_position_vec = self.get_world_position()
        spherical = world_position_vec.get_spherical_as_list()
        spherical[0] += 0.2  # Add a bit of offset between the cue and the text
        world_position_vec.set_spherical(spherical[0], spherical[1], spherical[2])

        # Get cartesian coordinates for plotting
        x, y, z = world_position_vec.get_cartesian_as_list()

        # Add the text to the axes. Position, label, and direction
        ax.text(x, y, z, label_str, (x, y, z))
