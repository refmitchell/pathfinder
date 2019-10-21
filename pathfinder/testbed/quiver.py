# Generate a basic quiver plot (vectors) inside a sphere

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.quiver([0,0,0],[0,0,0],[0,0,0],[0,0,1],[0,1,0],[1,0,0], normalize=True, color=['r','g','b'])

    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the surface
    ax.plot_surface(x, y, z, alpha=0.1, color='black')

    plt.show()