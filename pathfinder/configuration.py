"""
Module to contain the configuration information loaded from the config file.

DO NOT MODIFY THIS FILE!

Use yaml files in configurations directory to change the settings.
"""

# Optional settings (set defaults)
show_labels = False
show_geometry = False
show_individual = False
display_legend = True
combination_strategy = "avg"
confidence_threshold = 0
light_multiplier = 1
wind_multiplier = 1

# Cue configuration lists
cues_roll_one = []
cues_roll_two = []


def print_configuration():
    print("=== Optional configuration ===\n"
          "show-labels: " + str(show_labels) + "\n"
          "show-geometry: " + str(show_geometry) + "\n"
          "show-individual: " + str(show_individual) + "\n"
          "display-legend: " + str(display_legend) + "\n"
          "combination-strategy: " + combination_strategy + "\n"
          "confidence-threshold: " + str(confidence_threshold) + "\n"
          "light-multiplier: " + str(light_multiplier) + "\n"
          "wind-multiplier:  " + str(wind_multiplier) + "\n"                                                       
          "===============================\n")
