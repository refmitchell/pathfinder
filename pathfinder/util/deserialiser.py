from pathfinder.definitions import CONFIG_FILE
from pathfinder.world.light import Light
from pathfinder.world.wind import Wind

import yaml
import numpy as np


class Deserialiser:
    """
    Class to deserialise a pyyaml config file into the objects available.
    """
    def __init__(self, configuration_path=CONFIG_FILE):
        self.__config_path = configuration_path

    def __get_params_as_float(self, param_string):
        params = param_string.split(",")  # Deconstruct the parameters
        params = [p.strip() for p in params]  # Strip whitespace
        params = [float(p) for p in params]  # Convert to floats
        return params

    def __decode_light_parameters(self, dict):
        """
        Decode a light yaml specification into a Light object
        :param dict: The dictionary containing the light parameters
        :return: The Light object defined by the parameters
        """

        # If the length is zero then there is no configuration info and nothing to do.
        if len(dict) == 0:
            return Light()

        strength = 1
        elevation = np.pi/4
        azimuth = np.pi/2

        if "strength" in dict:
            strength = dict["strength"]
        if "elevation" in dict:
            elevation = np.radians(dict["elevation"])
        if "azimuth" in dict:
            azimuth = np.radians(dict["azimuth"])

        return Light(strength=strength, elevation=elevation, azimuth=azimuth)

    def __decode_wind_parameters(self, dict):
        """
        Decode wind parameters into a Wind object
        :param dict: The dictionary containing the wind parameters
        :return: The Wind object defined by the parameters
        """

        # If the length is zero then there is no configuration info and nothing to do.
        if len(dict) == 0:
            return Wind()

        strength = 1
        direction = np.pi/2

        if "strength" in dict:
            strength = dict["strength"]
        if "direction" in dict:
            direction = np.radians(dict["direction"])

        return Wind(strength=strength, direction=direction)

    def get_configuration(self):
        """
        Decodes the cues from the config.yaml file and generates the corresponding
        objects.
        :return: A list containing two lists, one with the cue objects for the first roll
        and another with the cue objects for the second roll.
        """
        full_cue_list = []
        with open(self.__config_path) as config:
            data = yaml.load_all(config, Loader=yaml.FullLoader)
            for doc in data:
                cues = doc['cues']
                cues_for_this_roll = []
                for name, parameters in cues.items():
                    # Add an elif for each cue
                    if "light" in name:
                        cues_for_this_roll.append(self.__decode_light_parameters(parameters))
                    elif "wind" in name:
                        cues_for_this_roll.append(self.__decode_wind_parameters(parameters))

                full_cue_list.append(cues_for_this_roll)

        return full_cue_list
