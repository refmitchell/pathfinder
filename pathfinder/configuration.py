"""
Module to contain the configuration information loaded from the config file.

DO NOT MODIFY THIS FILE!

Use config.yaml to change the settings.
"""

# Optional settings (set defaults)
show_labels = False
show_geometry = False
show_individual = False
combination_strategy = "sum"

# Cue configuration lists
cues_roll_one = []
cues_roll_two = []


def print_configuration():
    print("=== Optional configuration ===\n"
          "show-labels: " + str(show_labels) + "\n"
          "show-geometry: " + str(show_geometry) + "\n"
          "show-individual: " + str(show_individual) + "\n"
          "combination-strategy: " + combination_strategy + "\n"
          "===============================\n")
