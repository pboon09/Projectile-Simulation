import math
import json
import sys
sys.path.insert(0, 'Function')
from ProjectileFunction import *
from TrajectoryPathGenerator import *
from TargetGenerator import *

def FindPitch(yaw, input_target_z, base_target_distance, luncher_length, triangle_side_length):
    target_z = input_target_z - triangle_side_length/2
    adjustable_range = luncher_length * math.cos(math.radians(yaw))
    target_distance = base_target_distance + adjustable_range

    perfect_pitch = math.degrees(math.atan(target_z / target_distance))

    smallest_error = float('inf')
    pitch = None

    theta = -21
    while theta <= 21:
        error = abs(theta - perfect_pitch)
        if error < smallest_error:
            smallest_error = error  
            pitch = theta

        theta+=3
    return pitch

def FindYaw(base_target_distance, base_target_height, base_wall_distance, base_wall_height, luncher_length, luncher_base_height, velocity):
    min_error = float('inf')
    yaw = None
    
    for theta in range(24, 61, 3):
        adjustable_height = luncher_length * math.sin(math.radians(theta))
        target_height = base_target_height - adjustable_height - luncher_base_height

        adjustable_range = luncher_length * math.cos(math.radians(theta))
        target_distance = base_target_distance + adjustable_range

        tof = calculate_time_of_flight(velocity, theta, target_distance)
        hat = calculate_height_at_time(velocity, theta, tof)
        
        error = abs(hat - target_height)
        if error < min_error:
            min_error = error
            yaw = theta

    return yaw

def Calculate(Z_Target, Y_Target):
    z = Z_Target
    y = Y_Target

    # Constants (m)
    with open('Simulation Calculation\\config.json', 'r') as config_file:
        config = json.load(config_file)

    luncher_length = config["luncher_parameters"]["luncher_length"]
    luncher_baseHight = config["luncher_parameters"]["luncher_baseHight"]
    velocity = config["luncher_parameters"]["velocity"]
    table = config["field_parameters"]["table"]
    target_distance = config["field_parameters"]["target_distance"]
    wall_distance = config["field_parameters"]["wall_distance"]
    wall_height = config["field_parameters"]["wall_height"]
    triangle_side_length = config["target_parameters"]["triangle_side_length"]
    circle_diameter = config["target_parameters"]["circle_diameter"]
    squash_ball_diameter = config["target_parameters"]["squash_ball_diameter"]

    # Input for program (m)
    input_target_z = z/100 
    input_target_y =  y/100 + table

    Yaw = FindYaw(target_distance, input_target_y, wall_distance, wall_height, luncher_length, luncher_baseHight, velocity)
    Pitch = FindPitch(Yaw, input_target_z, target_distance, luncher_length, triangle_side_length)

    # #Input for plotting
    # trajectory_data = [{
    #     "theta": Y_Deg,
    #     "v0": target_speed, 
    #     "y0": luncher_length * math.sin(math.radians(Y_Deg)),#ไม่แก้
    #     "x0": -luncher_length * math.cos(math.radians(Y_Deg))#ไม่แก้
    # }]

    # position_data = [{
    #     "x": (math.tan(math.radians(X_Deg)) * (target_distance + (luncher_length * math.cos(math.radians(Y_Deg))))) + triangle_side_length/2,
    #     "y": tgh + luncher_length * math.sin(math.radians(Y_Deg)) - table,
    #     "diameter": squash_ball_diameter #ไม่แก้
    # }]

    # with open('Simulation Calculation\\TrajectoryPath.json', 'w') as file:
    #     json.dump(trajectory_data, file, indent=4)

    # with open('Simulation Calculation\\SquashBall_Pos.json', 'w') as file:
    #     json.dump(position_data, file, indent=4)

    # TargetInside = plot_Target_view(triangle_side_length, input_target_z, input_target_y - table, circle_diameter, 'Simulation Calculation\SquashBall_Pos.json')
    # plt.savefig('Picture\\Target.png')

    # plot_Path_view(target_distance, input_target_y, circle_diameter, 'Simulation Calculation\TrajectoryPath.json')
    # plt.savefig('Picture\\Trajectory.png')

    # # plt.show()
    # return X_Deg, Y_Deg, TargetInside
