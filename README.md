# Pathfinder: a tool for modelling dung beetle cue combination strategies. #
Contact: s1432329@sms.ed.ac.uk

## Requirements ##
- Anaconda (Python 3.7 version) (https://www.anaconda.com/distribution/#download-section)
- Matplotlib (via Anaconda)
- Numpy (via Anaconda)
- JupyterLab (via Anaconda)
- PyYAML (via Anaconda)
- IPywidgets (via Anaconda)

## Setup ##
Clone or download the repository to a location of your choice, we'll call this INSTALL_DIR.

Install Anaconda (Python 3.7) using the instructions/download available here:
https://www.anaconda.com/distribution/#download-section

Once you have Anaconda installed you need to create a virtual environment. On
linux use:

`$: conda create --name pathfinder`

Once you have created your virtual environment, activate it with:

`$: conda activate pathfinder`

You need to install Matplotlib, Numpy, JupyterLab, IPyWidgets and PyYAML to use
the tool. These can be installed with:

`$: conda install numpy matplotlib jupyterlab pyyaml ipywidgets`

Once the libraries are installed, you can run the application from
INSTALL_DIR/pathfinder with:

`$: jupyter notebook`

There are two notebooks: 'General' and 'Wind and Light'. The former is for
general usage the latter is a simplified version which allows configuration
of one wind cue and one light cue. See each for detailed information.

You can deactivate the virtual environment with:

`$: conda deactivate`

The software was developed on Linux (Ubuntu) and has not been tested on any other
platforms, however there is no linux-specific
code. Following the equivalent Anaconda setup on Windows/Mac should work. If you
experience problems with other platforms please get in touch. Miniconda should
also work if you're short on space, but again, this hasn't been tested.
