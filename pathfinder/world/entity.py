"""
Superclass to represent all world entities. An entity is anything in the world which
can be drawn in the display plot. Every Entity should have an origin. Hypothetically
this is the point around which the entity should be drawn. In almost all cases
this will be (0,0,0) so the default argument is the default Vec3 constructor which
corresponds to a zero vector centred at the origin.

All Entities should also implement a method to allow them to be drawn in the world.
"""

from pathfinder.util.vec3 import Vec3


class Entity:
    def __init__(self, origin=Vec3(magnitude=0, theta=0, phi=0)):
        self.__origin = origin

    def origin(self):
        return self.__origin

    def add_to_world(self, ax):
        """
        Add this entity to the world.
        :param ax: The Axes3D object representing the world plot.
        :return: Unused
        """
        ax.plot(self.__origin)