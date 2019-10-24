"""
Superclass defining all basic properties for all cues.
All cues have a position (as a Vec3) and a strength.

Default for a cue is placed at the origin with no strength.

Cue is essentially a special case of entity which has additional properties.
"""

from pathfinder.world.entity import Entity
from pathfinder.util.vec3 import Vec3, projection

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
        self.__label_position = self.__world_position.copy()
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

        # Check that elevation is between 0 and pi/2, azimuth doesn't matter.
        if self.__elevation > np.pi/2:
            self.__elevation = np.pi/2
        elif self.__elevation < 0:
            self.__elevation = 0

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

    def set_label_position(self, positional_vector):
        """
        Override the label position if required.
        :param positional_vector: A Vec3 which describes where the label should go
        :return: Unused
        """
        self.__label_position = positional_vector

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

    # Universal drawing code; this is needed for all cues.
    def add_to_world(self, ax):
        self.add_optional_elements(ax)

    def add_optional_elements(self, ax):
        """
        Check the configuration switches and add the desired output to the world.
        :param ax:
        :return: Unused
        """
        if conf.show_labels:
            self.add_label_to_world(ax)
        if conf.show_individual:
            self.show_individual(ax)
        if conf.show_geometry:
            self.add_geometry_to_world(ax)

    def add_label_to_world(self, ax):
        """
        Adds the cue label to the world
        :param ax: The Axes3D object which holds the world
        :return: Unused
        """
        label_str = self.__name

        # Generate label position
        label_position_vec = self.__label_position.copy()  # Use a copy because we need to modify this
        spherical = label_position_vec.get_spherical_as_list()
        spherical[0] += 0.05  # Add a bit of offset between the cue and the text
        label_position_vec.set_spherical(spherical[0], spherical[1], spherical[2])

        # Get cartesian coordinates for plotting
        x, y, z = label_position_vec.get_cartesian_as_list()

        # Add the text to the axes. Position, label, and direction
        ax.text(x, y, z, label_str, (x, y, z))

    def add_geometry_to_world(self, ax):
        """
        Adds the geometric vectors to the world
        :param ax: The Axes3D object which holds the world
        :return: Unused
        """
        geometric_vector = self.get_vector_description()
        o_x, o_y, o_z = [[x] for x in self.origin().get_cartesian_as_list()]
        geo_x, geo_y, geo_z = [[x] for x in geometric_vector.get_cartesian_as_list()]

        # Not 2D so I don't need the scaling parameters
        ax.quiver(o_x, o_y, o_z, geo_x, geo_y, geo_z, color='tab:gray', arrow_length_ratio=0.1)

    def show_individual(self, ax):
        """
        Shows the projection of individual cue vectors on the ground.
        :param ax: The Axes3D world object.
        :return: Unused
        """
        # Retrieve the spherical parameters of the world positional vector

        geo_vector = self.get_vector_description()
        geo_list = geo_vector.get_spherical_as_list()

        # The resultant vector pitched down so it runs along the ground, required
        # for projection unless I define a plane.
        ground_vector = Vec3(magnitude=geo_list[0],
                             theta=np.pi/2,
                             phi=geo_list[2])

        # Project the result onto the ground vector, gives a direction and a
        # "confidence" in its length
        projected_result = projection(geo_vector, ground_vector)

        o_x, o_y, o_z = [[x] for x in self.origin().get_cartesian_as_list()]
        proj_x, proj_y, prox_z = [[x] for x in projected_result.get_cartesian_as_list()]

        # Not 2D so I don't need the scaling parameters
        ax.quiver(o_x, o_y, o_z, proj_x, proj_y, prox_z, color='tab:brown', arrow_length_ratio=0.1)
