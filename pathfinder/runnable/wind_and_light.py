"""
Dedicated script for wind and light tests
-
Expected usage: user configures cues in the jupyter notebook using the slider widgets. The notebook will use only
                one wind cue and one light cue.
"""

# Pathfinder imports
from pathfinder.runnable.general import main
from pathfinder.util.serialiser import Serialiser

# Import the required widget resources
from ipywidgets import interactive, Layout
import ipywidgets as w


# Define a function to pack the widget data into a YAML compliant dictionary
# which can be processed by the software.
def update_config(
        show_individual,
        display_legend,
        show_sensory,
        combination_strategy,
        confidence_threshold,
        light_strength_one,
        light_elevation_one,
        light_azimuth_one,
        wind_strength_one,
        wind_direction_one,
        light_strength_two,
        light_elevation_two,
        light_azimuth_two,
        wind_strength_two,
        wind_direction_two
):
    config_dict = {
        "settings": {
            "show-individual": show_individual,
            "display-legend" : display_legend,
            "show-sensory": show_sensory,
            "combination-strategy": combination_strategy,
            "confidence-threshold": confidence_threshold
        },
        "cues-roll-one": {
            "light-0": {
                "strength": light_strength_one,
                "elevation": light_elevation_one,
                "azimuth": light_azimuth_one
            },
            "wind-0": {
                "strength": wind_strength_one,
                "direction": wind_direction_one
            }
        },
        "cues-roll-two": {
            "light-0": {
                "strength": light_strength_two,
                "elevation": light_elevation_two,
                "azimuth": light_azimuth_two
            },
            "wind-0": {
                "strength": wind_strength_two,
                "direction": wind_direction_two
            }
        }
    }
    write_out_to_config(config_dict)


# Define the interactive control widgets
def generate_controls():
    controls = interactive(
        update_config,
        {'manual': True},
        show_individual=w.Checkbox(value=False, description="Show individual cues "),
        display_legend=w.Checkbox(value=False, description="Enable/disable the legend "),
        show_sensory=w.Checkbox(value=False, description="Show sensory vectors "),

        combination_strategy=w.Dropdown(
            options=["avg", "wta", "proj_wta"],
            value="avg",
            description="Combination strategy: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}),

        confidence_threshold=w.BoundedFloatText(
            value=0.14,
            min=0,
            max=1,
            step=0.01,
            description="Confidence threshold: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}
        ),

        light_strength_one=w.FloatText(
            value=1,
            step=0.01,
            description="Roll one - light strength: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}
        ),

        light_elevation_one=w.FloatSlider(
            value=45,
            min=0,
            max=90,
            step=0.1,
            description="Roll one - light elevation: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}),

        light_azimuth_one=w.FloatSlider(
            value=45,
            min=-180,
            max=180,
            step=0.1,
            description="Roll one - light azimuth: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}),

        wind_strength_one=w.FloatText(
            value=1,
            step=0.01,
            description="Roll one - wind strength: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}
        ),

        wind_direction_one=w.FloatSlider(
            value=90,
            min=-180,
            max=180,
            step=0.1,
            description="Roll one - wind direction: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}),

        light_strength_two=w.FloatText(
            value=1,
            step=0.01,
            description="Roll two - light strength: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}
        ),

        light_elevation_two=w.FloatSlider(
            value=45,
            min=0,
            max=90,
            step=0.1,
            description="Roll two - light elevation: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}),

        light_azimuth_two=w.FloatSlider(
            value=45,
            min=-180,
            max=180,
            step=0.1,
            description="Roll two - light azimuth: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}),

        wind_strength_two=w.FloatText(
            value=1,
            step=0.01,
            description="Roll two - wind strength: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"}
        ),

        wind_direction_two=w.FloatSlider(
            value=90,
            min=-180,
            max=180,
            step=0.1,
            description="Roll two - wind direction: ",
            layout=Layout(width='50%'),
            style={"description_width": "initial"})
    )

    return controls


def write_out_to_config(config_dictionary):
    """
    Function which will take input from jupyter notebook in the form of a yaml compliant dictionary.
    The function passes the dictionary to the serialiser which auto-creates a config from it.
    :param config_dictionary: The configuration data in a yaml compliant dictionary format
    :return: Unused.
    """
    filename = "wind_and_light_jupyter_auto_conf.yaml"
    Serialiser.write_configuration_dictionary_to_file(config_dictionary, filename)
    main(filename)


if __name__ == '__main__':
    # For testing only
    generate_controls()
