from pathfinder.world.entity import Entity
from pathfinder.world.cue import Cue
from pathfinder.util.vec3 import Vec3, vector_sum_list, projection, angle_between_degrees, angle_between_azimuthal

import numpy as np


class Beetle(Entity):
    def __init__(self, strategy="avg"):
        super().__init__()
        # Unit vector pointing along the x-axis. Beetle always goes in this
        # direction on the first roll for simplicity
        self.__first_roll = Vec3(magnitude=1, theta=np.pi / 2, phi=0)
        self.__first_cue = Vec3(magnitude=1, theta=np.pi / 2, phi=0)
        self.__second_roll = Vec3(magnitude=1, theta=np.pi / 2, phi=0)
        self.__second_cue = Vec3(magnitude=1, theta=np.pi / 2, phi=0)
        self.__angle_offset = angle_between_azimuthal(self.__first_roll, self.__first_cue)
        self.__strategy = strategy

    def get_result_string(self):
        change_in_bearing = angle_between_degrees(self.__first_roll, self.__second_roll)
        result_string = "Change in bearing: " + str(change_in_bearing)

        return result_string

    def compute_first_path(self, cues):
        self.__first_cue = self.__compute_combined_cue(cues)
        self.__angle_offset = angle_between_azimuthal(self.__first_roll, self.__first_cue)

    def compute_second_path(self, cues):
        self.__second_cue = self.__compute_combined_cue(cues)
        cue_vec_list = self.__second_cue.get_spherical_as_list()
        print("Offset from cue-vector: " + str(self.__angle_offset))
        self.__second_roll = Vec3(magnitude=1,
                                  theta=cue_vec_list[1],
                                  phi=(cue_vec_list[2] + self.__angle_offset))

    def __compute_combined_cue(self, cues):
        """
        Given a list of cues and a strategy this method will set the beetles initial
        bearing.
        :param cues: A list of Cue objects.
        :return: Unused
        """
        if self.__strategy == "avg":
            vector_descriptions = [x.get_vector_description() for x in cues]
            resultant_vector = vector_sum_list(vector_descriptions)

            # Unpack the cartesian coordinates and divide by number of cues to
            # get a mean response vector
            resultant_list = resultant_vector.get_cartesian_as_list()
            resultant_list = [x/len(cues) for x in resultant_list]

            # Repack the average values into the Vec3 object
            resultant_vector.set_cartesian(resultant_list[0],
                                           resultant_list[1],
                                           resultant_list[2])
            resultant_list = resultant_vector.get_spherical_as_list()

            # The resultant vector pitched down so it runs along the ground, required
            # for projection unless I define a plane.
            ground_vector = Vec3(magnitude=resultant_list[0],
                                 theta=np.pi/2,
                                 phi=resultant_list[2])

            # Project the result onto the ground vector, gives a direction and a
            # "confidence" in its length
            projected_result = projection(resultant_vector, ground_vector)

            return projected_result

        elif self.__strategy == "wta":
            print(self.__strategy)

    def add_to_polar(self, ax, draw_bearing_change=False):
        """
        Draw the beetle's path onto the 2D polar axes.
        :param ax: 2D polar axes for display.
        :param draw_bearing_change: Boolean, set to tru if you want to draw the beetle's second roll.
        :return: Unused
        """
        origin_theta = 0
        origin_radius = 0        # Plot a point to represent the beetle

        ax.plot(origin_theta, origin_radius, color='black', marker='o', markersize=3)

        # Plot the first roll
        first_roll_2D = self.__first_roll.get_polar_as_list()
        first_cue_2D = self.__first_cue.get_2D_cartesian_as_list(modifier=100)

        print(first_roll_2D)
        print(first_cue_2D)

        # In format for quiver plots
        first_roll = [[x] for x in first_roll_2D]
        first_cue = [[x] for x in first_cue_2D]

        # Being lazy
        ax.quiver(origin_theta, origin_radius, first_roll[0], first_roll[1], color='black')

        # ax.quiver(origin_theta, origin_radius, first_cue[0], first_cue[1], color='red')

    def add_to_world(self, ax, draw_bearing_change=False):
        """
        Add the "beetle" to the world.
        :param ax: The Axes3D which represents the world
        :param draw_bearing_change: Boolean, set True if you want to draw the beetle's second roll.
        :return: Unused
        """
        origin = self.origin().get_cartesian_as_list()
        origin = [[x] for x in origin]
        # Plot a point to represent the beetle
        ax.plot(origin[0], origin[1], origin[2], color='black', marker='o', markersize=10)

        # Plot a vector showing the beetle's direction under a given set of cues
        first_roll = [[x] for x in self.__first_roll.get_cartesian_as_list()]
        ax.quiver(origin[0],
                  origin[1],
                  origin[2],
                  first_roll[0],
                  first_roll[1],
                  first_roll[2],
                  arrow_length_ratio=0.1,
                  color='black'
                  )

        first_cue = [[x] for x in self.__first_cue.get_cartesian_as_list()]
        ax.quiver(origin[0],
                  origin[1],
                  origin[2],
                  first_cue[0],
                  first_cue[1],
                  first_cue[2],
                  arrow_length_ratio=0.1,
                  color='red'
                  )

        if draw_bearing_change:
            second_roll = [[x] for x in self.__second_roll.get_cartesian_as_list()]
            # Colour are broken so plot separately
            ax.quiver(origin[0],
                      origin[1],
                      origin[2],
                      second_roll[0],
                      second_roll[1],
                      second_roll[2],
                      arrow_length_ratio=0.1,
                      color='green'
                      )
            second_cue = [[x] for x in self.__second_cue.get_cartesian_as_list()]
            ax.quiver(origin[0],
                      origin[1],
                      origin[2],
                      second_cue[0],
                      second_cue[1],
                      second_cue[2],
                      arrow_length_ratio=0.1,
                      color='orange'
                      )

