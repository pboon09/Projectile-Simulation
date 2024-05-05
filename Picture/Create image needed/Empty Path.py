import matplotlib.pyplot as plt # type: ignore
from matplotlib.patches import Circle # type: ignore
import numpy as np # type: ignore
import json

def projectile_motion(v0, theta, y0, x0, g=9.81):
    theta = np.radians(theta)
    t_flight = 2 * (v0 * np.sin(theta) + np.sqrt((v0 * np.sin(theta))**2 + 2 * g * y0)) / g
    t = np.linspace(0, t_flight, num=1000)

    x = x0 + v0 * np.cos(theta) * t
    y = y0 + v0 * np.sin(theta) * t - 0.5 * g * t**2

    return x, y

def plot_Path_view():   
    dpi = 100
    fig_width = 1281 / dpi
    fig_height = 540 / dpi

    plt.figure(figsize=(fig_width, fig_height), dpi=dpi)

    wall_x = [1, 1]
    wall_y = [0, 0.6]
    plt.plot(wall_x, wall_y, color='red', linewidth=2, label="Wall")

    plt.title("Trajectory path")
    plt.xlabel("X coordinate (m)")
    plt.ylabel("Y coordinate (m)")
    plt.ylim(bottom=0)
    plt.grid(True)
    plt.legend()
    plt.xlim(left=-0.5, right=5)
    plt.ylim(bottom=0, top=1.25)

    plt.tight_layout()

plot_Path_view()
plt.savefig("Picture\EmptyTarjectory.png")
# plt.show()