# Pathfinder: a tool for predicting dung beetle menotactic behaviour #
Contact: s1432329@sms.ed.ac.uk

## Requirements ##
- Anaconda (Python 3.7 version) (https://www.anaconda.com/distribution/#download-section)
- Matplotlib (via Anaconda)
- Numpy (via Anaconda)
- JupyterLab (via Anaconda)

## Setup ##
Clone the repository to a location of your choice, we'll call this INSTALL_DIR.

Once you have Anaconda installed you need to create a virtual environment. On
linux use:

`$: conda create --name pathfinder`

Once you have created your virtual environment, activate it with:

`$: conda activate pathfinder`

You need to install matplotlib, numpy, and jupyterlab to use the tool. These
can be installed with:

`$: conda install numpy matplotlib jupyterlab`

Once the libraries are installed, you can run the application from
INSTALL_DIR/pathfinder with:

`$: jupyter notebook`

The notebook should explain the rest!

You can deactivate the virtual environment with:

`$: conda deactivate`

