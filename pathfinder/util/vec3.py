"""
Class to hold a 3D vector in both a cartesian and spherical representation.
Spherical coordinates are needed within the code to define the geometry but they must be
translated to cartesian to be plotted. Hence, this class to handle the tedium.
"""

import numpy as np


def sum(a, b):
    """
    Vector sum of two 3D vectors
    :param a: Vec3 to be summed
    :param b: Vec3 to be summed
    :return: Vec3 object containing a + b
    """
    point_list = zip(a.get_cartesian_as_list(), b.get_cartesian_as_list())
    resultant_vector_as_list = [v1 + v2 for (v1, v2) in point_list]
    resultant_vector = Vec3()
    resultant_vector.set_cartesian(
        resultant_vector_as_list[0],
        resultant_vector_as_list[1],
        resultant_vector_as_list[2]
        )
    return resultant_vector


def sum_list(vector_list):
    """
    Sum a list of vectors to a single resultant vector.
    :param vector_list: A list of Vec3 objects to be summed.
    :return: The sum of the list.
    """
    vector_list = [x.get_cartesian_as_list() for x in vector_list]
    x = sum([v[0] for v in vector_list])
    y = sum([v[1] for v in vector_list])
    z = sum([v[2] for v in vector_list])
    resultant_vector = Vec3()
    resultant_vector.set_cartesian(x, y, z)
    return resultant_vector


class Vec3:
    def __init__(self, magnitude=0, theta=0, phi=0):
        """
        :param magnitude: Desired vector magnitude
        :param theta: Desired elevation angle
        :param phi: Desired azimuthal angle
        """
        # Internal representation of spherical coordinates
        # Internal coordinate system representations should not be
        # modified except through getters and setters
        self.__r = magnitude
        self.__theta = theta
        self.__phi = phi

        # Compute cartesian coordinates
        self.__x = self.__r * np.sin(self.__theta) * np.cos(self.__phi)
        self.__y = self.__r * np.sin(self.__theta) * np.sin(self.__phi)
        self.__z = self.__r * np.cos(self.__theta)

    def set_cartesian(self, x, y, z):
        """
        This method will update the cartesian coordinates of the vector object.
        The spherical coordinates will be updated to match. Usage is not recommended
        as all displays use a spherical coordinate system.

        :param x: Cartesian x coordinate
        :param y: Cartesian y coordinate
        :param z: Cartesian z coordinate
        :return: Unused

        """
        self.__x = x
        self.__y = y
        self.__z = z

        # Recompute spherical coordinates
        self.__r = np.sqrt(x**2 + y**2 + z**2)
        self.__phi = np.arctan2(y, x)
        self.__theta = np.arccos(z/self.__r)

    def set_spherical(self, magnitude, theta, phi):
        """
        Sets the spherical coordinates manually and updates the cartesian
        representation to match. Spherical coordinates use the physics convention of
        theta for inclination and phi for azimuth for the simple purpose that I can't read.

        :param magnitude: Desired vector magnitude
        :param theta: inclination angle (in radians)
        :param phi: Azimuthal angle (in radians)
        :return: Unused
        """
        self.__r = magnitude
        self.__theta = theta
        self.__phi = phi

        # Recompute cartesian coordinates
        self.__x = self.__r * np.sin(self.__theta) * np.cos(self.__phi)
        self.__y = self.__r * np.sin(self.__theta) * np.sin(self.__phi)
        self.__z = self.__r * np.cos(self.__theta)

    def get_cartesian_as_list(self):
        """
        :return: A list of the cartesian coordinates of the vector. [x, y, z]
        """
        return [self.__x, self.__y, self.__z]

    def get_spherical_as_list(self):
        """
        :return: A list of the spherical coordinates of the vector. [r, t, p]
        """
        return [self.__r, self.__theta, self.__phi]

    def get_both_as_list(self):
        """
        :return: Both sets of coordinates as a 2D list, [[r, t, p],[x, y, z]]
        """
        return [self.get_spherical_as_list(), self.get_cartesian_as_list()]

