import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import json

# Function to calculate the projectile motion trajectory
def projectile_motion(v0, theta, y0, x0, g=9.81):
    theta = np.radians(theta)  # Convert angle to radians
    # Calculate the time of flight based on initial velocity, angle, and initial height
    t_flight = 2 * (v0 * np.sin(theta) + np.sqrt((v0 * np.sin(theta))**2 + 2 * g * y0)) / g
    t = np.linspace(0, t_flight, num=1000)  # Generate time intervals

    # Calculate the x and y coordinates over time
    x = x0 + v0 * np.cos(theta) * t
    y = y0 + v0 * np.sin(theta) * t - 0.5 * g * t**2

    return x, y

# Function to plot the trajectory path along with the target
def plot_Path_view(circle_target_x, circle_target_y, diameter_circle, json_file_path):
    # Set the DPI and figure size for the plot
    dpi = 100
    fig_width = 1281 / dpi
    fig_height = 540 / dpi

    plt.figure(figsize=(fig_width, fig_height), dpi=dpi)

    # Load trajectory data from a JSON file
    with open(json_file_path, 'r') as file:
        trajectories = json.load(file)

    # Loop through each trajectory data and plot the projectile motion
    for i, data in enumerate(trajectories):
        v0 = data['v0']  # Initial velocity
        theta = data['theta']  # Launch angle
        y0 = data['y0']  # Initial height
        x0 = data.get('x0', -0.3)  # Initial x position, default to -0.3 if not specified
        
        x, y = projectile_motion(v0, theta, y0, x0)  # Calculate trajectory
        
        # Plot the trajectory
        plt.plot(x, y, label=f"Target at Angle {theta}°")
        
        # Plot the initial vertical position line
        plt.vlines(x0, 0, y0, colors='black', linestyles='dashed')

    # Plot a red vertical line representing the wall
    wall_x = [1, 1]
    wall_y = [0, 0.6]
    plt.plot(wall_x, wall_y, color='red', linewidth=2, label="Wall")

    # Plot the target circle
    circle = Circle((circle_target_x, circle_target_y), diameter_circle / 2, color='green', fill=False, label="Target A")
    plt.gca().add_patch(circle)

    # Set plot titles and labels
    plt.title("Trajectory path")
    plt.xlabel("X coordinate (m)")
    plt.ylabel("Y coordinate (m)")
    plt.ylim(bottom=0)  # Set y-axis lower limit
    plt.grid(True)  # Add grid to the plot
    plt.legend()  # Add legend to the plot
    plt.xlim(left=-0.5, right=5)  # Set x-axis limits
    plt.ylim(bottom=0, top=1.25)  # Set y-axis limits

    plt.tight_layout()  # Adjust layout for better fit
