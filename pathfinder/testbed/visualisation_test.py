# Generate a basic quiver plot (vectors) inside a sphere with a dot acting as a "light".

# Basic visualisation exercise in matplotlib

from mpl_toolkits.mplot3d import Axes3D  # This seems to be required, though PyCharm disagrees
import matplotlib.pyplot as plt
import matplotlib.colors as cls
import numpy as np

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    r = 1
    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    zss = r * np.outer(np.ones(np.size(u)), np.cos(v))
    zss = [[z if z >= 0 else 0 for z in zs] for zs in zss]  # Remove all negative z
    z = np.array(zss)

    light = cls.LightSource(azdeg=0, altdeg=45)
    #z = zs

    # Define an arbitrary point acting as a light cue, if lighting can't be done in mpl
    # could draw a Gaussian around it to create an intensity pattern.
    radius = 1
    gamma = np.pi / 8  # 45deg, also should be phi
    theta = np.pi / 4  # 90deg

    # Define cartesian coordinates (lists to make life easy with ax.plot)
    light_x = [radius * np.sin(theta) * np.cos(gamma)]
    light_y = [radius * np.sin(theta) * np.sin(gamma)]
    light_z = [radius * np.cos(theta)]

    # Plot the surface and the axes vectors
    ax.plot(light_x, light_y, light_z, color='orange', marker='o', markersize=12)
    ax.plot_surface(x, y, z, alpha=0.1, lightsource=light)
    ax.quiver([0,0,0],[0,0,0],[0,0,0],[0,0,1],[0,1,0],[1,0,0], color=['r','g','b'], arrow_length_ratio=0.1)

    # Axes properties
    ax.set_axis_off()
    ax.set_zlim([0, 1])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    plt.show()