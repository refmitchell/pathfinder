from pathfinder.definitions import CONFIG_FILE
from pathfinder.world.light import Light
from pathfinder.world.wind import Wind
from pathfinder.world.polarisation_filter import PolarisationFilter

import pathfinder.configuration as conf

import yaml
import numpy as np


#
# This file is inherently messy. Need to account for a lot of optional configuration and store configuration
# globally.
#
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

    def __decode_light_parameters(self, name, dict):
        """
        Decode a light yaml specification into a Light object
        :param dict: The dictionary containing the light parameters
        :return: The Light object defined by the parameters
        """

        # If the length is zero then there is no configuration info and nothing to do.
        if len(dict) == 0:
            return Light(name)

        strength = 1
        elevation = np.pi/4
        azimuth = np.pi/2

        if "strength" in dict:
            strength = dict["strength"]
        if "elevation" in dict:
            elevation = np.radians(dict["elevation"])
        if "azimuth" in dict:
            azimuth = np.radians(dict["azimuth"])

        return Light(name, strength=strength, elevation=elevation, azimuth=azimuth)

    def __decode_wind_parameters(self, name, dict):
        """
        Decode wind parameters into a Wind object
        :param dict: The dictionary containing the wind parameters
        :return: The Wind object defined by the parameters
        """

        # If the length is zero then there is no configuration info and nothing to do.
        if len(dict) == 0:
            return Wind(name)

        strength = 1
        direction = np.pi/2

        if "strength" in dict:
            strength = dict["strength"]
        if "direction" in dict:
            direction = np.radians(dict["direction"])

        return Wind(name, strength=strength, direction=direction)

    def __decode_polarisation_parameters(self, name, dict):
        if len(dict) == 0:
            return PolarisationFilter(name)

        strength = 1
        azimuth = 0

        if "strength" in dict:
            strength = dict["strength"]
        if "azimuth" in dict:
            azimuth = np.radians(dict["azimuth"])

        return PolarisationFilter(name, strength=strength, azimuth=azimuth)

    def __decode_global_settings(self, settings):
        """
        Decode and set optional global settings, set in conf module from here.
        :param settings: The dictionary with the settings.
        :return: Unused.
        """
        if 'show-labels' in settings:
            conf.show_labels = settings['show-labels']
        if 'show-sensory' in settings:
            conf.show_sensory = settings['show-sensory']
        if 'show-individual' in settings:
            conf.show_individual = settings['show-individual']
        if 'combination-strategy' in settings:
            conf.combination_strategy = settings['combination-strategy']
        if 'confidence-threshold' in settings:
            conf.confidence_threshold = settings['confidence-threshold']
        if 'display-legend' in settings:
            conf.display_legend = settings['display-legend']
        if 'cue-strength-scaling' in settings:
            # More nested options so delegate.
            self.__decode_scaling_parameters(settings['cue-strength-scaling'])

    def __decode_scaling_parameters(self, scaling):
        """
        Decode and set optional cue scaling parameters which set multipliers for the strength of each cue.
        :param scaling: The dictionary with the scaling section
        :return: Unused.
        """
        if 'light' in scaling:
            conf.light_multiplier = scaling['light']
        if 'wind' in scaling:
            conf.wind_multiplier = scaling['wind']
        if 'polarisation' in scaling:
            conf.polarisation_multiplier = scaling['polarisation']

    def __decode_cues(self, cuedefs):
        """
        Decode cues from yaml format into a list of Cue objects, returned to be set
        from calling function.
        :param cuedefs: The dictionary of cue definitions for a single roll
        :return: The list of cues.
        """
        cues_for_this_roll = []
        for name, parameters in cuedefs.items():
            # Add an elif for each cue
            if "light" in name:
                cues_for_this_roll.append(self.__decode_light_parameters(name, parameters))
            elif "wind" in name:
                cues_for_this_roll.append(self.__decode_wind_parameters(name, parameters))
            elif "polarisation" in name:
                cues_for_this_roll.append(self.__decode_polarisation_parameters(name, parameters))

        return cues_for_this_roll

    def init_configuration(self):
        """
        Decodes the cues from the config.yaml file and generates the corresponding objects.
        Objects are then saved to a central configuration module.

        :return: A 2D list of the cues for each roll, should use conf directly though.
        """
        with open(self.__config_path) as config:
            data = yaml.load(config, Loader=yaml.FullLoader)

            # Check existence of configuration switches then call the relevant functions
            if 'settings' in data:
                self.__decode_global_settings(data['settings'])
            if 'cues-roll-one' in data:
                conf.cues_roll_one = self.__decode_cues(data['cues-roll-one'])
            if 'cues-roll-two' in data:
                conf.cues_roll_two = self.__decode_cues(data['cues-roll-two'])

            conf.print_configuration()

        return [conf.cues_roll_one, conf.cues_roll_two]
