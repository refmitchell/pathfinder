"""
Class to represent the world axes which may be plotted
"""
import numpy as np

from pathfinder.util.vec3 import Vec3
from pathfinder.world.entity import Entity


class DevAxes(Entity):
    #
    # Init: DevAxes needs a figure to draw on.
    #
    def __init__(self, magnitude=0.5):
        """
        Define a set of 3 vectors to act as development axes in the coordinate system of
        the dome world.

        :param magnitude:
        """
        super().__init__()

        #
        # Define three vectors for x,y,z axes relative to the plot
        # X-Axis: phi = 0, theta = pi/2, r = magnitude
        # Y-Axis: phi = pi/2, theta = pi/2, r = magnitude
        # Z-Axis: phi = pi/2, theta = 0, r = magnitude
        #

        # Spherical parameters
        r = magnitude
        x_phi = 0
        x_theta = np.pi/2
        y_phi = np.pi / 2
        y_theta = np.pi / 2
        z_phi = np.pi / 2
        z_theta = 0

        # Define the axes
        self.__x_vector = Vec3(r, x_theta, x_phi)
        self.__y_vector = Vec3(r, y_theta, y_phi)
        self.__z_vector = Vec3(r, z_theta, z_phi)

    def get_axes_cartesian(self):
        """
        :return: A list of Vec3 objects representing the x, y, and z development.
        """
        return [self.__x_vector, self.__y_vector, self.__z_vector]

    def add_to_world(self, ax):
        origin = self.origin().get_cartesian_as_list()
        x = self.__x_vector.get_cartesian_as_list()
        y = self.__y_vector.get_cartesian_as_list()
        z = self.__z_vector.get_cartesian_as_list()
        ax.quiver(origin, origin, origin, x, y, z, color=['b','k','k'], arrow_length_ratio=0.1)


class DevCompassMarkings(Entity):
    def __init__(self):
        """
        Development class to show basic compass markings for the bottom circle
        """
        super().__init__()

        # Define a vector for each point on the compass: 0, 90, 180, 270
        self.__points = [Vec3(magnitude=1, theta=np.pi/2),
                         Vec3(magnitude=1, phi=-np.pi/2, theta=np.pi/2),
                         Vec3(magnitude=1, phi=np.pi, theta=np.pi/2),
                         Vec3(magnitude=1, phi=np.pi/2, theta=np.pi/2)]

        self.__labelvecs = [Vec3(magnitude=1.2, theta=np.pi / 2),
                            Vec3(magnitude=1.2, phi=-np.pi / 2, theta=np.pi / 2),
                            Vec3(magnitude=1.2, phi=np.pi, theta=np.pi / 2),
                            Vec3(magnitude=1.2, phi=np.pi / 2, theta=np.pi / 2)]

    def add_to_world(self, ax):
        points_for_drawing = [[[y] for y in x.get_cartesian_as_list()] for x in self.__points]
        label_vecs_for_drawing = [x.get_cartesian_as_list() for x in self.__labelvecs]
        labels = ["0", "90", "180", "-90"]

        for i in range(4):
            point = points_for_drawing[i]
            label_vec = label_vecs_for_drawing[i]
            ax.plot(point[0], point[1], point[2], color='black', marker='o', markersize=5)
            ax.text(label_vec[0], label_vec[1], label_vec[2], labels[i])
            i += 1
