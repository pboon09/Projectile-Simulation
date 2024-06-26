import matplotlib.pyplot as plt
import numpy as np
import json

# Function to generate and plot an equilateral triangle
def generate_triangle(ax, side_length):
    # Define the vertices of the triangle
    x0, y0 = 0, 0
    x1 = side_length
    y1 = 0
    height = (np.sqrt(3)/2) * side_length
    x2 = side_length / 2
    y2 = height
    
    # Create the triangle vertices list
    triangle_x = [x0, x1, x2, x0]
    triangle_y = [y0, y1, y2, y0]
    
    # Plot the triangle
    ax.plot(triangle_x, triangle_y, 'r-', linewidth=2)
    ax.fill(triangle_x, triangle_y, 'orange', alpha=0.5)
    
    return [(x0, y0), (x1, y1), (x2, y2)]

# Function to generate and plot a circle
def generate_circle(ax, center_z, center_y, diameter, color='white'):
    radius = diameter / 2
    circle = plt.Circle((center_z, center_y), radius, color=color, fill=True)
    ax.add_patch(circle)
    return (center_z, center_y), radius

# Function to check if a circle is completely inside a triangle
def is_circle_in_triangle(center, radius, vertices):
    # Helper function to check if a point is inside a triangle using barycentric coordinates
    def point_in_triangle(pt, v1, v2, v3):
        d1 = sign(pt, v1, v2)
        d2 = sign(pt, v2, v3)
        d3 = sign(pt, v3, v1)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

    # Helper function to calculate the sign of an area
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    # Check the distance from the center of the circle to each side of the triangle
    for i in range(3):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % 3]
        d = np.abs(np.cross(np.subtract(p2, p1), np.subtract(p1, center)) / np.linalg.norm(np.subtract(p2, p1)))
        if d < radius:
            return False

    # Check if all points around the circle are inside the triangle
    step_angle = np.pi / 4  # Check 8 points around the circle
    for angle in np.arange(0, 2 * np.pi, step_angle):
        edge_point = (center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle))
        if not point_in_triangle(edge_point, *vertices):
            return False

    return True

# Function to plot the target view including the triangle and circles
def plot_Target_view(side_length_m, target_center_z_m, target_center_y_m, target_diameter_m, json_file_path):
    # Convert measurements to centimeters
    side_length_cm = round(side_length_m * 100, 2)
    target_center_z_cm = round(target_center_z_m * 100, 2)
    target_center_y_cm = round(target_center_y_m * 100, 2)
    target_diameter_cm = round(target_diameter_m * 100, 2)

    # Set the DPI and size for the plot
    dpi = 100
    size_in_inches = 540 / dpi

    # Create the plot
    fig, ax = plt.subplots(figsize=(size_in_inches, size_in_inches), dpi=dpi)
    vertices = generate_triangle(ax, side_length_cm)

    # Generate and plot the target circle
    center, radius = generate_circle(ax, target_center_z_cm, target_center_y_cm, target_diameter_cm)
    if not is_circle_in_triangle(center, radius, vertices):
        return False

    # Load additional positions from a JSON file
    with open(json_file_path, 'r') as file:
        black_positions = json.load(file)

    # Plot each additional position as a black circle
    for position in black_positions:
        black_center_z_cm = position['z'] * 100
        black_center_y_cm = position['y'] * 100
        black_diameter_cm = position['diameter'] * 100
        black_center, black_radius = generate_circle(ax, black_center_z_cm, black_center_y_cm, black_diameter_cm, 'black')
        center2, radius2 = generate_circle(ax, black_center_z_cm, black_center_y_cm, 0.1)

    # Set plot limits and labels
    ax.set_xlim(0, side_length_cm)
    ax.set_ylim(0, (np.sqrt(3)/2) * side_length_cm)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.1)
    ax.set_title('Target View')
    ax.set_xlabel('Z coordinate (cm)')
    ax.set_ylabel('Y coordinate (cm)')

    return True
