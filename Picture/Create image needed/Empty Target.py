import matplotlib.pyplot as plt
import numpy as np
import json

def generate_triangle(ax, side_length):
    x0, y0 = 0, 0
    x1 = side_length
    y1 = 0
    height = (np.sqrt(3)/2) * side_length
    x2 = side_length / 2
    y2 = height
    triangle_x = [x0, x1, x2, x0]
    triangle_y = [y0, y1, y2, y0]
    ax.plot(triangle_x, triangle_y, 'r-', linewidth=2)
    ax.fill(triangle_x, triangle_y, 'orange', alpha=0.5)
    return [(x0, y0), (x1, y1), (x2, y2)]

def generate_circle(ax, center_z, center_y, diameter):
    radius = diameter / 2
    circle = plt.Circle((center_z, center_y), radius, color='white', fill=True)
    ax.add_patch(circle)
    return (center_z, center_y), radius

def generate_black_circle(ax, center_z, center_y, diameter):
    radius = diameter / 2
    black_circle = plt.Circle((center_z, center_y), radius, color='black', fill=True, zorder=3)
    ax.add_patch(black_circle)
    return (center_z, center_y), radius

def is_circle_in_triangle(center, radius, vertices):
    for i in range(3):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % 3]
        d = np.abs(np.cross(np.subtract(p2, p1), np.subtract(p1, center)) / np.linalg.norm(np.subtract(p2, p1)))
        if d < radius:
            return False
    return True

def plot_Target_view(side_length_m, target_center_z_m, target_center_y_m, target_diameter_m, json_file_path):
    side_length_cm = round(side_length_m * 100, 2)
    target_center_z_cm = round(target_center_z_m * 100, 2)
    target_center_y_cm = round(target_center_y_m * 100, 2)

    dpi = 100
    size_in_inches = 540 / dpi

    fig, ax = plt.subplots(figsize=(size_in_inches, size_in_inches), dpi=dpi)
    vertices = generate_triangle(ax, side_length_cm)

    ax.set_xlim(0, side_length_cm)
    ax.set_ylim(0, (np.sqrt(3)/2) * side_length_cm)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.1)
    ax.set_title('Target View')
    ax.set_xlabel('Z coordinate (cm)')
    ax.set_ylabel('Y coordinate (cm)')

    print(f"Distance from left to center: {target_center_z_cm} cm")
    print(f"Distance from bottom to center: {target_center_y_cm} cm")

plot_Target_view(0.5, 0.35, 0.0875, 0.137, 'Simulation Calculation\SquashBall_Pos.json')
plt.savefig("Picture\EmptyTarget.png")
