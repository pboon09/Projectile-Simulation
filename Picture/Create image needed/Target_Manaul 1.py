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

def generate_circle(ax, center_x, center_y, diameter):
    radius = diameter / 2
    circle = plt.Circle((center_x, center_y), radius, color='white', fill=True)
    ax.add_patch(circle)
    return (center_x, center_y), radius

def generate_black_circle(ax, center_x, center_y, diameter):
    radius = diameter / 2
    black_circle = plt.Circle((center_x, center_y), radius, color='black', fill=True, zorder=3)
    ax.add_patch(black_circle)
    return (center_x, center_y), radius

def is_circle_in_triangle(center, radius, vertices):
    for i in range(3):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % 3]
        d = np.abs(np.cross(np.subtract(p2, p1), np.subtract(p1, center)) / np.linalg.norm(np.subtract(p2, p1)))
        if d < radius:
            return False
    return True

def plot_Target_view(side_length_m, target_center_x_m, target_center_y_m, target_diameter_m, json_file_path):
    side_length_cm = round(side_length_m * 100, 2)
    target_center_x_cm = round(target_center_x_m * 100, 2)
    target_center_y_cm = round(target_center_y_m * 100, 2)
    target_diameter_cm = round(target_diameter_m * 100, 2)

    fig, ax = plt.subplots(figsize=(6, 5))
    vertices = generate_triangle(ax, side_length_cm)

    center, radius = generate_circle(ax, target_center_x_cm, target_center_y_cm, target_diameter_cm)

    if not is_circle_in_triangle(center, radius, vertices):
            raise ValueError(f"The target at ({target_center_x_cm}, {target_center_y_cm}) is not inside the triangle")

    ax.plot([0, center[0]], [center[1], center[1]], 'r-', linewidth = 4)  # Red horizontal line
    ax.plot([center[0], center[0]], [0, center[1]], 'b-', linewidth = 4)  # Blue vertical line

    black_center, black_radius = generate_black_circle(ax, target_center_x_cm, target_center_y_cm, 1)

    ax.set_xlim(0, side_length_cm)
    ax.set_ylim(0, (np.sqrt(3)/2) * side_length_cm)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.1)
    ax.set_title('Target View')
    ax.set_xlabel('Z coordinate (cm)')
    ax.set_ylabel('Y coordinate (cm)')

    print(f"Distance from left to center: {target_center_x_cm} cm")
    print(f"Distance from bottom to center: {target_center_y_cm} cm")

plot_Target_view(0.5, 0.35, 0.0875, 0.137, 'Simulation Calculation\SquashBall_Pos.json')
plt.show()
