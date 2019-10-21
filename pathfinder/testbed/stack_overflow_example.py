import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')

    # Plot origin (agent's start point)
    ax.plot(0, 0, color='black', marker='o', markersize=5)

    # Plot agent's path
    ax.quiver((0, 0), (0, 1), color='black')

    # Example of where (0, 1) should be
    ax.plot(0, 1, color='black', marker='o', markersize=5)

    # Plot configuration
    ax.set_rticks([])
    ax.set_rmin(0)
    ax.set_rmax(1)
    ax.set_thetalim(-np.pi, np.pi)
    ax.set_xticks(np.linspace(np.pi, -np.pi, 4, endpoint=False))

    ax.grid(False)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("N")

    plt.show()
