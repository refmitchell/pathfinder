"""
Class to hold a 3D vector in both a cartesian and spherical representation.
Spherical coordinates are needed within the code to define the geometry but they must be
translated to cartesian to be plotted. Hence, this class to handle the tedium.
"""

import numpy as np


def dot_product(a, b):
    # Compute the scalar and return it
    return sum(
        [x1*x2 for (x1, x2) in zip(a.get_cartesian_as_list(), b.get_cartesian_as_list())]
    )


def projection(a, b):
    """
    Project a onto ("the line parallel to") b
    :param a: Vec3
    :param b: Vec3
    :return: The projected result
    """
    # Get normalised b vector
    b_list = b.get_spherical_as_list()
    b.set_spherical(magnitude=1, theta=b_list[1], phi=b_list[2])

    # Compute the magnitude of the projected vector
    a1 = dot_product(a, b)

    # Return a vector in the direction of b(_normal) but with the length
    # of the projection
    return Vec3(magnitude=a1, theta=b_list[1], phi=b_list[2])


def vector_sum(a, b):
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


def vector_sum_list(vector_list):
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


def angle_between_degrees(a, b):
    """
    Get the angle between Vec3s a and b
    :param a: Vec3
    :param b: Vec3
    :return: The angle between the two vectors in degrees
    """
    scalar_product = dot_product(a, b)
    mag_a = a.get_spherical_as_list()[0]
    mag_b = b.get_spherical_as_list()[0]
    cosine_of_angle = scalar_product / (mag_a * mag_b)
    angle = np.arccos(cosine_of_angle)
    return np.rad2deg(angle)


def angle_between_radians(a, b):
    """
    Get the angle between Vec3s a and b
    :param a: Vec3
    :param b: Vec3
    :return: The angle between the two vectors in radians
    """
    scalar_product = dot_product(a, b)
    mag_a = a.get_spherical_as_list()[0]
    mag_b = b.get_spherical_as_list()[0]
    cosine_of_angle = scalar_product / (mag_a * mag_b)
    angle = np.arccos(cosine_of_angle)
    return angle


def angle_between_azimuthal(a, b):
    """
    Take the straight signed azimuthal difference between a and b
    :param a: Vec3
    :param b: Vec3
    :return: a.phi - b.phi
    """
    a = a.get_spherical_as_list()
    b = b.get_spherical_as_list()
    return a[2] - b[2]


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

    def copy(self):
        """
        Get a copy of this Vec3
        :return: A new Vec3 object with the same r, theta, and phi
        """
        return Vec3(magnitude=self.__r, theta=self.__theta, phi=self.__phi)

    def get_polar_as_list(self):
        """
        Get 2D polar coordinates, r and phi
        :return: a list containing r and phi
        """
        r = self.__r if self.__r <= 1 else 1
        return [-self.__phi, r]
