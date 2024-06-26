import math
import json
import sys
sys.path.insert(0, 'Function')
from ProjectileFunction import *
from TrajectoryPathGenerator import *
from TargetGenerator import *

# Function to find the optimal pitch angle
def FindPitch(Pitch_min, Pitch_max, Pitch_step, yaw, input_target_z, base_target_distance, luncher_length, triangle_side_length):
    # Calculate the target z coordinate relative to the triangle center
    target_z = input_target_z - triangle_side_length/2
    # Calculate the adjustable range of the launcher based on yaw angle
    adjustable_range = luncher_length - (luncher_length * math.cos(math.radians(yaw)))
    target_distance = base_target_distance + adjustable_range

    # Calculate the perfect pitch angle
    perfect_pitch = math.degrees(math.atan(target_z / target_distance))

    smallest_error = float('inf')
    pitch = None

    # Iterate through the possible pitch angles to find the one with the smallest error
    for theta in range(Pitch_min, Pitch_max + 1, Pitch_step):
        error = abs(theta - perfect_pitch)
        if error < smallest_error:
            smallest_error = error  
            pitch = theta

    return pitch

# Function to find the optimal yaw angle
def FindYaw(Yaw_min, Yaw_max, Yaw_step, base_target_distance, base_target_height, base_wall_distance, base_wall_height, luncher_length, luncher_base_height, velocity, circle_diameter):
    min_error = float('inf')
    yaw = None
    
    # Iterate through the possible yaw angles to find the one with the smallest error
    for theta in range(Yaw_min, Yaw_max + 1, Yaw_step):
        # Calculate the adjustable height and range based on yaw angle
        adjustable_height = luncher_length * math.sin(math.radians(theta))
        target_height = base_target_height - adjustable_height - luncher_base_height
        wall_height = base_wall_height - adjustable_height - luncher_base_height
        adjustable_range = luncher_length - (luncher_length * math.cos(math.radians(theta)))
        target_distance = base_target_distance + adjustable_range
        wall_distance = base_wall_distance + adjustable_range

        # Calculate the time of flight and height at that time
        tof = calculate_time_of_flight(velocity, theta, target_distance)
        hat = calculate_height_at_time(velocity, theta, tof)

        # Define the bounds for target height
        UpperBound = target_height + circle_diameter/2
        LowerBound = target_height - circle_diameter/2

        # Check if the projectile hits the wall
        HitWall = check_wall_collision(theta, velocity, wall_distance, wall_height)
        
        if not HitWall and hat + 0.02 < UpperBound and hat - 0.02 > LowerBound:
            error = abs(hat - target_height)
            if error < min_error:
                min_error = error
                yaw = theta

    return yaw

# Main function to calculate pitch, yaw, and if the target is inside
def Calculate(Z_Target, Y_Target):
    z = Z_Target
    y = Y_Target

    # Constants (m)
    with open('Simulation Calculation\\config.json', 'r') as config_file:
        config = json.load(config_file)

    # Extract parameters from config file
    luncher_length = config["luncher_parameters"]["luncher_length"]
    luncher_baseHight = config["luncher_parameters"]["luncher_baseHight"]
    velocity = config["luncher_parameters"]["velocity"]
    Pitch_min = config["luncher_parameters"]["Pitch_min"]
    Pitch_max = config["luncher_parameters"]["Pitch_max"]
    Pitch_step = config["luncher_parameters"]["Pitch_step"]
    Yaw_min = config["luncher_parameters"]["Yaw_min"]
    Yaw_max = config["luncher_parameters"]["Yaw_max"]
    Yaw_step = config["luncher_parameters"]["Yaw_step"]
    table = config["field_parameters"]["table"]
    target_distance = config["field_parameters"]["target_distance"]
    wall_distance = config["field_parameters"]["wall_distance"]
    wall_height = config["field_parameters"]["wall_height"]
    triangle_side_length = config["target_parameters"]["triangle_side_length"]
    circle_diameter = config["target_parameters"]["circle_diameter"]
    squash_ball_diameter = config["target_parameters"]["squash_ball_diameter"]

    # Convert target coordinates to meters and adjust for table height
    input_target_z = z / 100 
    input_target_y = y / 100 + table

    # Find the optimal yaw and pitch angles
    Yaw = FindYaw(Yaw_min, Yaw_max, Yaw_step, target_distance, input_target_y, wall_distance, wall_height, luncher_length, luncher_baseHight, velocity, circle_diameter)
    Pitch = FindPitch(Pitch_min, Pitch_max, Pitch_step, Yaw, input_target_z, target_distance, luncher_length, triangle_side_length)

    # Input for plotting
    trajectory_data = [{
        "theta": Yaw,
        "v0": velocity, 
        "y0": luncher_length * math.sin(math.radians(Yaw)) + luncher_baseHight,
        "x0": -(luncher_length - luncher_length * math.cos(math.radians(Yaw)))
    }]

    # Calculate the height at the target distance
    tgh = calculate_height_at_time(velocity, Yaw, calculate_time_of_flight(velocity, Yaw, target_distance))

    # Prepare position data for plotting
    position_data = [{
        "z": (math.sin(math.radians(Pitch)) * (target_distance + (luncher_length * math.cos(math.radians(Pitch))))) + triangle_side_length/2,
        "y": tgh + luncher_length * math.sin(math.radians(Yaw)) + luncher_baseHight - table,
        "diameter": squash_ball_diameter
    }]

    # Save trajectory and position data to JSON files
    with open('Simulation Calculation\\TrajectoryPath.json', 'w') as file:
        json.dump(trajectory_data, file, indent=4)

    with open('Simulation Calculation\\SquashBall_Pos.json', 'w') as file:
        json.dump(position_data, file, indent=4)

    # Plot the target view and trajectory path
    TargetInside = plot_Target_view(triangle_side_length, input_target_z, input_target_y - table, circle_diameter, 'Simulation Calculation\\SquashBall_Pos.json')
    plt.savefig('Picture\\Target.png')

    plot_Path_view(target_distance, input_target_y, circle_diameter, 'Simulation Calculation\\TrajectoryPath.json')
    plt.savefig('Picture\\Trajectory.png')

    return Pitch, Yaw, TargetInside
