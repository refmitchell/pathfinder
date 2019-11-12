import yaml
import os
from pathfinder.definitions import CONFIG_DIR


class Serialiser:
    @staticmethod
    def write_configuration_dictionary_to_file(dictionary, filename):
        """
        Write a configuration to a .yaml file. Dictionary and filename are not checked.

        Only really needed for jupyter notebook.
        :param dictionary: Configuration in a dictionary format.
        :param filename:
        :return: Unused
        """
        proposed_path = os.path.join(CONFIG_DIR, filename)
        with open(proposed_path, "w+") as outfile:
            yaml.dump(dictionary, outfile, default_flow_style=False)

