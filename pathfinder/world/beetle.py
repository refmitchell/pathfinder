from pathfinder.world.entity import Entity
from pathfinder.world.cue import Cue
from pathfinder.util.vec3 import Vec3, vector_sum_list, projection, angle_between_degrees, angle_between_azimuthal
import pathfinder.util.colours as colours


import pathfinder.configuration as conf

import numpy as np
from pylab import Circle


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
        self.__strategy = conf.combination_strategy
        self.__confidence_threshold = conf.confidence_threshold

    def get_result_string(self):
        change_in_bearing = angle_between_degrees(self.__first_roll, self.__second_roll)
        result_string = "Absolute change in bearing: " + str(np.abs(change_in_bearing))
        confidence = self.__first_cue.get_spherical_as_list()[0]
        confidence_two = self.__second_cue.get_spherical_as_list()[0]
        print("Confidence in first cue: " + str(confidence))
        print("Confidence in second cue: " + str(confidence_two))
        return result_string

    def compute_first_path(self, cues):
        self.__first_cue = self.__compute_combined_cue(cues)
        self.__angle_offset = angle_between_azimuthal(self.__first_roll, self.__first_cue)

    def compute_second_path(self, cues):
        self.__second_cue = self.__compute_combined_cue(cues)
        cue_vec_list = self.__second_cue.get_spherical_as_list()

        self.__second_roll = Vec3(magnitude=1,
                                  theta=cue_vec_list[1],
                                  phi=(cue_vec_list[2] + self.__angle_offset))

    def add_to_polar(self, ax, draw_bearing_change=False):
        """
        Draw the beetle's path onto the 2D polar axes.
        :param ax: 2D axes for display.
        :param draw_bearing_change: Boolean, set to tru if you want to draw the beetle's second roll.
        :return: Unused
        """
        o_x = 0
        o_y = 0

        # Plot the beetle start point
        ax.plot(o_x, o_y, color=colours.BEETLE_COLOUR, marker='o', markersize=5)

        # Plot the first roll
        first_roll = self.__first_roll.get_polar_as_list()
        first_cue = self.__first_cue.get_polar_as_list()

        # Quiver plot
        ax.quiver(o_x,
                  o_y,
                  [first_roll[0], first_cue[0]],
                  [first_roll[1], first_cue[1]],
                  color=[colours.BEETLE_ROLL_ONE_COLOUR, colours.ROLL_ONE_CUE_COLOUR],
                  angles='xy',
                  scale_units='xy',
                  scale=1)

        if draw_bearing_change:
            # Plot the first roll
            second_roll = self.__second_roll.get_polar_as_list()
            second_cue = self.__second_cue.get_polar_as_list()

            # Quiver plot
            ax.quiver(o_x,
                      o_y,
                      [second_roll[0], second_cue[0]],
                      [second_roll[1], second_cue[1]],
                      color=[colours.BEETLE_ROLL_TWO_COLOUR, colours.ROLL_TWO_CUE_COLOUR],
                      angles='xy',
                      scale_units='xy',
                      scale=1)

        # If a confidence threshold has been set, draw it on the polar plot
        if self.__confidence_threshold > 0:

            confidence_ring = Circle(
                (0, 0),
                self.__confidence_threshold,
                alpha=0.3,
                color=colours.CONFIDENCE_THRESHOLD_COLOUR,
                transform=ax.transData._b # Required to get the circle to plot correctly in polar axes.
                )
            ax.add_artist(confidence_ring)

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
        ax.plot(origin[0], origin[1], origin[2], color=colours.BEETLE_COLOUR, marker='o', markersize=10)

        # Plot a vector showing the beetle's direction under a given set of cues
        first_roll = [[x] for x in self.__first_roll.get_cartesian_as_list()]
        ax.quiver(origin[0],
                  origin[1],
                  origin[2],
                  first_roll[0],
                  first_roll[1],
                  first_roll[2],
                  arrow_length_ratio=0.1,
                  color=colours.BEETLE_ROLL_ONE_COLOUR
                  )

        first_cue = [[x] for x in self.__first_cue.get_cartesian_as_list()]
        ax.quiver(origin[0],
                  origin[1],
                  origin[2],
                  first_cue[0],
                  first_cue[1],
                  first_cue[2],
                  arrow_length_ratio=0.1,
                  color=colours.ROLL_ONE_CUE_COLOUR
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
                      color=colours.BEETLE_ROLL_TWO_COLOUR
                      )
            second_cue = [[x] for x in self.__second_cue.get_cartesian_as_list()]
            ax.quiver(origin[0],
                      origin[1],
                      origin[2],
                      second_cue[0],
                      second_cue[1],
                      second_cue[2],
                      arrow_length_ratio=0.1,
                      color=colours.ROLL_TWO_CUE_COLOUR
                      )

    #
    # Private
    #

    def __compute_combined_cue(self, cues):
        """
        Given a list of cues this method will set the beetles initial
        bearing based on the strategy configured.
        :param cues: A list of Cue objects.
        :return: The resultant cue vector.
        """
        vector_descriptions = [x.get_scaled_vector_description() for x in cues]

        if self.__strategy == "avg":
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
            #
            # This is a strict winner take all which doesn't care about modality.
            # The strongest cue wins regardless of its type.
            #
            list_descriptions = [x.get_spherical_as_list() for x in vector_descriptions]
            magnitudes = [x[0] for x in list_descriptions]
            max_value = max(magnitudes)
            max_indices = [i for i, x in enumerate(magnitudes) if x == max_value]

            # If we have multiple strongest cues cannot make any decision about which
            # to follow.
            if len(max_indices) > 1:
                return Vec3(magnitude=0)

            # Return the vector with the greatest magnitude
            return vector_descriptions[magnitudes.index(max(magnitudes))]
