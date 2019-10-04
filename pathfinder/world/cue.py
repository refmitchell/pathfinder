"""
Superclass defining all basic properties for all cues.
All cues have a position (as a Vec3) and a strength.

Default for a cue is placed at the origin with no strength.

Cue is essentially a special case of entity which has additional properties.
"""

from pathfinder.world.entity import *
from pathfinder.util.vec3 import *


class Cue(Entity):
    def __init__(self, position=Vec3()):
        """
        Define a generic cue, positioned on the "position" vector.
        :param position: A Vec3 that describes the cue's position w.r.t. the world sphere

        """
        super().__init__()
        self.__position = position

    def set_position(self, position):
        self.__position = position

    def get_position(self):
        return self.__position

