import os
from enum import Enum

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, "configurations")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")
