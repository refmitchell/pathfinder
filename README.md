# Pathfinder: a tool for modelling dung beetle cue combination strategies. #
Contact: s1432329@sms.ed.ac.uk

## Requirements ##
- Anaconda (Python 3.7 version) (https://www.anaconda.com/distribution/#download-section)
- Matplotlib (via Anaconda)
- Numpy (via Anaconda)
- JupyterLab (via Anaconda)
- PyYAML (via Anaconda)

## Setup ##
Clone the repository to a location of your choice, we'll call this INSTALL_DIR.

Once you have Anaconda installed you need to create a virtual environment. On
linux use:

`$: conda create --name pathfinder`

Once you have created your virtual environment, activate it with:

`$: conda activate pathfinder`

You need to install Matplotlib, Numpy, JupyterLab, and PyYAML to use the tool.
These can be installed with:

`$: conda install numpy matplotlib jupyterlab pyyaml`

Once the libraries are installed, you can run the application from
INSTALL_DIR/pathfinder with:

`$: jupyter notebook`

The notebook should explain the rest!

You can deactivate the virtual environment with:

`$: conda deactivate`

The software has not been tested on Windows, however there is no linux-specific
code. Following the equivalent Anaconda setup on Windows should work. If you
experience problems with Windows please get in touch. Miniconda should also
work if you're short on space, but again, this hasn't been tested.
