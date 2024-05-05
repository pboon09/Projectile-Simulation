import math
import json
import sys
sys.path.insert(0, 'Function')
from ProjectileFunction import *
from TrajectoryPathGenerator import *
from TargetGenerator import *

def FindHorizontalSetting(Y_Deg, input_target_x, base_target_distance, luncher_lenght, triangle_side_length):
    input_target_x = input_target_x - triangle_side_length/2
    adjustable_range = luncher_lenght * math.cos(math.radians(Y_Deg))
    target_distance = base_target_distance + adjustable_range
    
    if target_distance <= 0:
        raise ValueError("Target distance must be positive")

    Perfect_X_Deg = math.degrees(math.atan(input_target_x / target_distance))
    
    smallest_error = float('inf')
    best_X_Deg = None

    theta = -30
    while theta <= 30:
        error = abs(theta - Perfect_X_Deg)
        if error < smallest_error:
            smallest_error = error  
            best_X_Deg = theta

        if -10 <= theta < 10:
            theta += 1
        else:
            theta += 5

    
    return best_X_Deg, Perfect_X_Deg

def GenerateAllPossibleTrajectory(base_target_distance, base_target_height, base_wall_distance, base_wall_height, luncher_lenght, json_file_path):
    results = []
    for theta in range(1,90):
        adjustable_height = luncher_lenght * math.sin(math.radians(theta))
        target_height = base_target_height - adjustable_height
        wall_height = base_wall_height - adjustable_height

        adjustable_range = luncher_lenght * math.cos(math.radians(theta))
        target_distance = base_target_distance + adjustable_range
        wall_distance = base_wall_distance + adjustable_range

        u = calculate_initial_velocity(theta, target_distance, target_height)
        tof = calculate_time_of_flight(u, theta, target_distance)
        trh = calculate_time_to_reach_height(u, theta, target_height)
        collide = check_wall_collision(theta, u, wall_distance, wall_height)
        hit = check_max_height(theta, u)
        if u is not None and not collide:
            results.append({
                "theta": theta,
                "initial_velocity": u,
                "time_of_flight": tof,
                "time_to_reach_height": trh,
                "collision": collide,
                "max_height": hit,
                "target_height": target_height,
                "adjustable_height": adjustable_height,
                "adjustable_range": adjustable_range
            })
    with open(json_file_path, 'w') as f:
        json.dump(results, f, indent=4)
    # print("Generated all possible trajectory data Done")

def FindVerticalSetting(json_file_path, input_target_y):
    with open(json_file_path, 'r') as file:
        trajectories = json.load(file)
    
    smallest_error = float('inf')
    best_Y_Deg = None
    Perfect_Y_Deg = None

    for trajectory in trajectories:
        theta = trajectory['theta']
        tof = trajectory['time_of_flight']
        trh = trajectory['time_to_reach_height']
        target_height = trajectory['target_height']
        collide = trajectory['collision']
        
        if not collide:
            time_difference = abs(tof - trh)
            height_difference = abs(input_target_y - target_height)
            combined_error = time_difference + height_difference
            
            if combined_error < smallest_error:
                smallest_error = combined_error
                Perfect_Y_Deg = trajectory['theta']

    valid_thetas = [25, 30, 35, 40, 45, 50, 55, 60]
    best_Y_Deg = min(valid_thetas, key=lambda x: abs(x - Perfect_Y_Deg))

    return best_Y_Deg, Perfect_Y_Deg

def Calculate(X_Target, Y_Target):
    # Input from user (cm) [measure from bottom left corner]
    # x = 15
    # y = 6.85

    x = X_Target
    y = Y_Target

    # Constants (m)
    target_distance = 2
    wall_distance = 1
    wall_height = 60/100
    triangle_side_length = 0.5
    circle_diameter = 0.137
    squash_ball_diameter = 0.04
    table = 75.5/100

    # Input for program (m)
    input_target_y =  y/100 + table
    input_target_x = x/100 
    luncher_lenght = 0.3

    GenerateAllPossibleTrajectory(target_distance, input_target_y, wall_distance, wall_height, luncher_lenght, 'Simulation Calculation\TrajectoryDataBase.json')
    Y_Deg, Perfect_Y_Deg = FindVerticalSetting('Simulation Calculation\TrajectoryDataBase.json', input_target_y)
    X_Deg, Perfect_X_Deg = FindHorizontalSetting(Y_Deg, input_target_x, target_distance, luncher_lenght, triangle_side_length)

    #Output for User
    print(f"X Degree: {X_Deg}, Y Degree: {Y_Deg}, Perfect X Degree: {round(Perfect_X_Deg,2)}, Perfect Y Degree: {Perfect_Y_Deg}")

    with open('Simulation Calculation\TrajectoryDataBase.json', 'r') as file:
        trajectories = json.load(file)

    for trajectory in trajectories:
        theta_data = trajectory['theta']
        if theta_data == Y_Deg:
            tgh = trajectory['target_height']
            target_speed = trajectory['initial_velocity']

    #edit herez
    # pressure_to_velocity = {
    #     6: 6.111,
    #     5: 6.019,
    #     4: 5.887,
    #     3: 5.646,
    #     2: 5.048,
    #     1: 2.948
    # }
    
    # Pressure = None
    # velo = None
    # smallest_difference = float('inf')
    
    # for p, velocity in pressure_to_velocity.items():
    #     difference = abs(velocity - target_speed)
        
    #     if difference < smallest_difference:
    #         smallest_difference = difference
    #         Pressure = p
    #         velo = velocity

    #Input for plotting
    trajectory_data = [{
        "theta": Y_Deg,
        # "v0": calculate_initial_velocity(Y_Deg, target_distance, tgh),
        "v0": target_speed,
        "y0": luncher_lenght * math.sin(math.radians(Y_Deg)),
        "x0": -luncher_lenght * math.cos(math.radians(Y_Deg))
    }]

    position_data = [{
        "x": (math.tan(math.radians(X_Deg)) * (target_distance + (luncher_lenght * math.cos(math.radians(Y_Deg))))) + triangle_side_length/2,
        "y": tgh + luncher_lenght * math.sin(math.radians(Y_Deg)) - table,
        "diameter": squash_ball_diameter
    }]

    with open('Simulation Calculation\\TrajectoryPath.json', 'w') as file:
        json.dump(trajectory_data, file, indent=4)

    with open('Simulation Calculation\\SquashBall_Pos.json', 'w') as file:
        json.dump(position_data, file, indent=4)

    plot_Target_view(triangle_side_length, input_target_x, input_target_y - table, circle_diameter, 'Simulation Calculation\SquashBall_Pos.json')
    plt.savefig('Picture\Target.png')

    plot_Path_view(target_distance, input_target_y, circle_diameter, 'Simulation Calculation\TrajectoryPath.json')
    plt.savefig('Picture\Trajectory.png')

    Pressure = 6
    
    # plt.show()
    return X_Deg, Y_Deg, Pressure
