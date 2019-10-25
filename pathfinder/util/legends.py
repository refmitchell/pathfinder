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
    handles.append(mlines.Line2D([], [], color=colours.BEETLE_ROLL_ONE_COLOUR, linestyle='-', label='First roll direction'))
    handles.append(mlines.Line2D([], [], color=colours.BEETLE_ROLL_TWO_COLOUR, linestyle='-', label='Second roll direction'))

    # Define legend for combined cues
    handles.append(mlines.Line2D([], [], color=colours.ROLL_ONE_CUE_COLOUR, linestyle='-', label='First roll combined cue'))
    handles.append(mlines.Line2D([], [], color=colours.ROLL_TWO_CUE_COLOUR, linestyle='-', label='Second roll combined cue'))

    # Add legend elements for optional stuff.
    if conf.show_individual:
        handles.append(mlines.Line2D([], [], color=colours.SCALED_PROJECTED_CUE_VECTOR_COLOUR, linestyle='-', label='Individual cue indicator'))
    if conf.show_geometry:
        handles.append(mlines.Line2D([], [], color=colours.SCALED_GEOMETRIC_CUE_VECTOR_COLOUR, linestyle='-', label='Geometric cue vector'))

    return handles


def create_polar_legend_handles():
    """
    Create a list of handles for a legend for the 2D bearing plots.
    :return: The list of handles for the legend
    """
    handles = []

    # Define legend for the beetle
    handles.append(mlines.Line2D([], [], color=colours.BEETLE_ROLL_ONE_COLOUR, linestyle='-', label='First roll direction'))
    handles.append(mlines.Line2D([], [], color=colours.BEETLE_ROLL_TWO_COLOUR, linestyle='-', label='Second roll direction'))

    # Define legend for combined cues
    handles.append(mlines.Line2D([], [], color=colours.ROLL_ONE_CUE_COLOUR, linestyle='-', label='First roll combined cue'))
    handles.append(mlines.Line2D([], [], color=colours.ROLL_TWO_CUE_COLOUR, linestyle='-', label='Second roll combined cue'))

    # If confidence threshold is defined, need a legend element for that too.
    if conf.confidence_threshold > 0:
        handles.append(mpatches.Patch(color=colours.CONFIDENCE_THRESHOLD_COLOUR, label='Cue confidence threshold'))

    return handles
