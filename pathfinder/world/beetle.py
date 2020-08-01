from pathfinder.world.entity import Entity
from pathfinder.world.cue import Cue
from pathfinder.world.polarisation_filter import PolarisationFilter, PolarisationFilterMirror
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
        print("Confidence in first combined cue: " + str(confidence))
        print("Confidence in second combined cue: " + str(confidence_two))
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
        roll_vector = self.__first_roll.get_polar_as_list()
        cue_vector = self.__first_cue.get_polar_as_list()

        if draw_bearing_change:
            # Plot the second roll
            roll_vector = self.__second_roll.get_polar_as_list()
            cue_vector = self.__second_cue.get_polar_as_list()

        print("Roll Vector length: " + str(len(roll_vector)))
        print("Cue Vector length: " + str(len(cue_vector)))
        
        # Quiver plot
        ax.quiver([o_x, o_x],
                  [o_y, o_y],
                  [roll_vector[0], cue_vector[0]],
                  [roll_vector[1], cue_vector[1]],
                  color=[colours.BEETLE_ROLL_COLOUR, colours.CUE_COLOUR],
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

        # Assume we're plotting the first roll
        roll_vector = [[x] for x in self.__first_roll.get_cartesian_as_list()]
        cue_vector = [[x] for x in self.__first_cue.get_cartesian_as_list()]

        if draw_bearing_change:
            # Correct if we're plotting the second
            roll_vector = [[x] for x in self.__second_roll.get_cartesian_as_list()]
            cue_vector = [[x] for x in self.__second_cue.get_cartesian_as_list()]

        # Plot the roll and cue vectors
        ax.quiver(
            origin[0],
            origin[1],
            origin[2],
            roll_vector[0],
            roll_vector[1],
            roll_vector[2],
            arrow_length_ratio=0.1,
            color=colours.BEETLE_ROLL_COLOUR
            )

        ax.quiver(
            origin[0],
            origin[1],
            origin[2],
            cue_vector[0],
            cue_vector[1],
            cue_vector[2],
            arrow_length_ratio=0.1,
            color=colours.CUE_COLOUR
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
            # If we don't care about polarisation, don't do a bunch of extra work.
            print("Polarisation defined: " + str(conf.polarisation_defined))
            if not conf.polarisation_defined:
                return self.__compute_avg_cue(cues)

            # Separate out polarisation and non-polarisation cues, non-pol go into two lists.
            pol_cues = [x for x in cues if isinstance(x, PolarisationFilter) or isinstance(x, PolarisationFilterMirror)]

            set_one = [
                x for x in cues if not (isinstance(x, PolarisationFilter) or isinstance(x, PolarisationFilterMirror))
            ]
            set_two = [
                x for x in cues if not (isinstance(x, PolarisationFilter) or isinstance(x, PolarisationFilterMirror))
            ]

            # Safe assumption that we have only one polarisation definition and hence only two polarisation cues,
            # the defined and the mirror.
            set_one.append(pol_cues[0])
            set_two.append(pol_cues[1])

            # Compute two separate combined cue vectors.
            combination_one = self.__compute_avg_cue(set_one)
            combination_two = self.__compute_avg_cue(set_two)

            # Retrieve magnitudes
            mag_one = combination_one.get_spherical_as_list()[0]
            mag_two = combination_two.get_spherical_as_list()[0]

            if mag_one > mag_two:
                # Combination one is stronger, use that.
                return combination_one
            elif mag_two > mag_one:
                # Combination two is stronger, use that.
                return combination_two

            # If we reach this statement they're equal in magnitude so pick one at random.
            r = np.random.rand()

            return combination_one if r > 0.5 else combination_two

        elif self.__strategy == "wta":
            #
            # This is a strict winner take all which doesn't care about modality.
            # The strongest cue wins regardless of its type.
            #
            list_descriptions = [x.get_spherical_as_list() for x in vector_descriptions]
            magnitudes = [x[0] for x in list_descriptions]
            max_value = max(magnitudes)
            max_indices = [i for i, x in enumerate(magnitudes) if x == max_value]

            # If we have multiple strongest cues either we cannot make any decision about which
            # to follow, or we have a polarising filter.

            if len(max_indices) > 1:
                strongest_cues = [cues[x] for x in max_indices]
                #strongest_cues = cues[max_indices]
                type_filter = [
                    x for x in strongest_cues
                    if isinstance(x, PolarisationFilter) or isinstance(x, PolarisationFilterMirror)
                ]

                # Multiple strongest cues, not all of which are polarisation, no decision can be made.
                if len(type_filter) != len(strongest_cues):
                    return Vec3(magnitude=0, theta=np.pi/2)

                # If the polarisation cue is strongest, we cannot disambiguate between the two directions so pick one
                # at random. Return the projection.
                rand_idx = np.random.randint(0, 1)
                winner = strongest_cues[rand_idx].get_scaled_vector_description()
                winner_list = winner.get_spherical_as_list()
                winner_ground = Vec3(magnitude=winner_list[0], theta=np.pi/2, phi=winner_list[2])
                return projection(winner, winner_ground)

            winner = vector_descriptions[magnitudes.index(max(magnitudes))]
            winner_sphere = winner.get_spherical_as_list()
            winner_ground = Vec3(magnitude=winner_sphere[0], theta=np.pi/2, phi=winner_sphere[2])
            winner_projection = projection(winner, winner_ground)

            # Return the vector with the greatest magnitude
            return winner_projection

        elif self.__strategy == "proj_wta":
            # Projected winner take all. We take the strongest vector of the projected cues. Arguably this makes
            # far more sense than strict wta.
            list_descriptions = [x.get_spherical_as_list() for x in vector_descriptions]
            ground_list_descriptions = [[x[0], np.pi/2, x[2]] for x in list_descriptions]
            ground_vectors = [Vec3(magnitude=x[0], theta=x[1], phi=x[2]) for x in ground_list_descriptions]
            projections = [projection(a, b) for (a, b) in zip(vector_descriptions, ground_vectors)]
            list_descriptions = [x.get_spherical_as_list() for x in projections]

            magnitudes = [x[0] for x in list_descriptions]
            max_value = max(magnitudes)
            max_indices = [i for i, x in enumerate(magnitudes) if x == max_value]

            # If we have multiple strongest cues cannot make any decision about which
            # to follow.
            if len(max_indices) > 1:
                strongest_cues = [cues[x] for x in max_indices]
                strongest_list_items = [list_descriptions[x] for x in max_indices]
                type_filter = [
                    x for x in strongest_cues
                    if isinstance(x, PolarisationFilter) or isinstance(x, PolarisationFilterMirror)
                ]

                # Multiple strongest cues, not all of which are polarisation, no decision can be made.
                if len(type_filter) != len(strongest_cues):
                    return Vec3(magnitude=0, theta=np.pi / 2)

                # If dealing with the polarisation cue, choose a direction at random amongst the two. Return the
                # projection.
                rand_idx = np.random.randint(0, 1)
                m, t, p = strongest_list_items[rand_idx]
                return Vec3(magnitude=m, theta=t, phi=p)

            max_idx = magnitudes.index(max(magnitudes))
            winner = vector_descriptions[max_idx]

            # Check cue type, polarisation results should be bimodal

            winner_sphere = winner.get_spherical_as_list()
            winner_ground = Vec3(magnitude=winner_sphere[0], theta=np.pi/2, phi=winner_sphere[2])
            winner_projection = projection(winner, winner_ground)
            
            # Return the vector with the greatest magnitude
            return winner_projection

    def __compute_avg_cue(self, cues):
        vector_descriptions = [x.get_scaled_vector_description() for x in cues]
        resultant_vector = vector_sum_list(vector_descriptions)

        # Unpack the cartesian coordinates and divide by number of cues to
        # get a mean response vector
        resultant_list = resultant_vector.get_cartesian_as_list()
        resultant_list = [x / len(vector_descriptions) for x in resultant_list]

        # Repack the average values into the Vec3 object
        resultant_vector.set_cartesian(resultant_list[0],
                                       resultant_list[1],
                                       resultant_list[2])
        resultant_list = resultant_vector.get_spherical_as_list()

        # The resultant vector pitched down so it runs along the ground, required
        # for projection unless I define a plane.
        ground_vector = Vec3(magnitude=resultant_list[0],
                             theta=np.pi / 2,
                             phi=resultant_list[2])

        # Project the result onto the ground vector, gives a direction and a
        # "confidence" in its length
        projected_result = projection(resultant_vector, ground_vector)

        return projected_result
