import math

def calculate_initial_velocity(theta_degrees, target_distance, target_height):
    theta_radians = math.radians(theta_degrees)
    g = 9.81
    sqrt_expression = g * target_distance**2 / (2 * math.cos(theta_radians)**2 * (math.tan(theta_radians) * target_distance - target_height))
    if sqrt_expression < 0:
        return None
    return math.sqrt(sqrt_expression)

def calculate_time_of_flight(initial_velocity, theta_degrees, distance):
    theta_radians = math.radians(theta_degrees)
    if initial_velocity is None:
        return None
    return distance / (initial_velocity * math.cos(theta_radians))

def calculate_time_to_reach_height(initial_velocity, theta_degrees, height):
    theta_radians = math.radians(theta_degrees)
    g = 9.81
    if initial_velocity is None:
        return None
    a = 0.5 * g
    b = -initial_velocity * math.sin(theta_radians)
    c = height
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    return max(t1, t2)

def check_wall_collision(theta_degrees, initial_velocity, wall_distance, wall_height):
    theta_radians = math.radians(theta_degrees)
    g = 9.81
    if initial_velocity is None:
        return None
    time_to_wall = wall_distance / (initial_velocity * math.cos(theta_radians))
    height_at_wall = initial_velocity * time_to_wall * math.sin(theta_radians) - 0.5 * g * time_to_wall**2
    return height_at_wall < wall_height

def check_max_height(theta_degrees, initial_velocity):
    theta_radians = math.radians(theta_degrees)
    g = 9.81

    if initial_velocity is None:
        return None
    
    height = ((initial_velocity**2) * (math.sin(theta_radians))**2)/(2*g)

    return height

def calculate_height_at_time(initial_velocity, theta_degrees, time):
    theta_radians = math.radians(theta_degrees)
    g = 9.81  # Acceleration due to gravity in m/s^2
    if initial_velocity is None:
        return None
    
    # Calculate vertical height at a given time
    height = (initial_velocity * time * math.sin(theta_radians)) - (0.5 * g * time**2)
    return height

def find_trajectory_ranges(base_target_distance, base_target_height, base_wall_distance, base_wall_height, luncher_lenght):
    max_theta, min_theta = 0, 90
    max_velocity, min_velocity = 0, float('inf')
    count = 0
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
            count += 1
            max_theta = max(max_theta, theta)
            min_theta = min(min_theta, theta)
            max_velocity = max(max_velocity, u)
            min_velocity = min(min_velocity, u)
            print("theta {}, u {:.4f}, tof-trh {:.4f}-{:.4f}, collide {}, hit-target {:.4f}-{:.4f}, adj height {:.4f}, adj range {:.4f}".format(theta,u,tof,trh, collide, hit,target_height, adjustable_height, adjustable_range))
    return min_theta, max_theta, min_velocity, max_velocity, count