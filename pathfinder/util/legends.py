import pathfinder.configuration as conf
import pathfinder.util.colours as colours

import matplotlib.lines as mlines
import matplotlib.patches as mpatches


def create_world_legend_handles():
    """
    Create a list of handles for a legend for the 3D world plots.
    :return: The list of handles for the legend
    """
    handles = []

    # Define legend for the beetle
    handles.append(
        mlines.Line2D([], [], color=colours.BEETLE_ROLL_COLOUR, linestyle='-', label='Chosen roll direction'))

    # Define legend for combined cues
    handles.append(mlines.Line2D([], [], color=colours.CUE_COLOUR, linestyle='-', label='Combined cue vector'))

    # Add legend elements for optional stuff.
    if conf.show_individual:
        handles.append(mlines.Line2D([], [], color=colours.SCALED_PROJECTED_CUE_VECTOR_COLOUR, linestyle='-', label='Individual cue indicator'))
    if conf.show_sensory:
        handles.append(mlines.Line2D([], [], color=colours.SCALED_GEOMETRIC_CUE_VECTOR_COLOUR, linestyle='-', label='Geometric cue vector'))

    return handles


def create_polar_legend_handles():
    """
    Create a list of handles for a legend for the 2D bearing plots.
    :return: The list of handles for the legend
    """
    handles = []

    # Define legend for the beetle
    handles.append(mlines.Line2D([], [], color=colours.BEETLE_ROLL_COLOUR, linestyle='-', label='Chosen roll direction'))

    # Define legend for combined cues
    handles.append(mlines.Line2D([], [], color=colours.CUE_COLOUR, linestyle='-', label='Combined cue vector'))

    # If confidence threshold is defined, need a legend element for that too.
    if conf.confidence_threshold > 0:
        handles.append(mpatches.Patch(color=colours.CONFIDENCE_THRESHOLD_COLOUR, label='Cue confidence threshold'))

    return handles
