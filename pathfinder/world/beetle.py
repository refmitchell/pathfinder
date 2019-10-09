from pathfinder.world.entity import Entity
from pathfinder.util.vec3 import Vec3, sum_list

import numpy as np


class Beetle(Entity):
    def __init__(self):
        super().__init__()
        # Unit vector pointing along the x-axis. Beetle always goes in this
        # direction on the first roll for simplicity
        self.__direction = Vec3(magnitude=1, theta=np.pi/2, phi=0)

    def set_initial_path(self, cues, strategy="sum"):
        """
        Given a list of cues and a strategy this method will set the beetles initial
        bearing.
        :param cues: A list of Cue objects.
        :param strategy: A strategy for combining cues. Supported: "sum",
        "wta" (winner-takes-all)
        :return: Unused
        """
        if strategy == "sum":
            vector_descriptions = [x.get_vector_description() for x in cues]
            # END POINT, add 'em up

        elif strategy == "wta":
            print(strategy)

    def add_to_world(self, ax):
        """
        Add the "beetle" to the world.
        :param ax: The Axes3D which represents the world
        :return: Unused
        """
        origin = self.origin().get_cartesian_as_list()
        origin = [[x] for x in origin]
        # Plot a point to represent the beetle
        ax.plot(origin[0], origin[1], origin[2], color='black', marker='o', markersize=10)

        # Plot a vector showing the beetle's direction
        direction = [[x] for x in self.__direction.get_cartesian_as_list()]
        ax.quiver(origin[0],
                  origin[1],
                  origin[2],
                  direction[0],
                  direction[1],
                  direction[2],
                  arrow_length_ratio=0.1,
                  color='black'
                  )
