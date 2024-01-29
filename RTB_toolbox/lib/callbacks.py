import os
import random
import csv
import numpy as np
from spatialgeometry import Sphere, Cuboid, CollisionShape
from spatialmath import SO3, SE3
import swift
import roboticstoolbox as rtb


def handle_path(file):
    """
    Generate the full path for a file located in the 'Resources' directory.

    This function takes a file name as an argument and returns the full path
    for the file, considering its potential location within the 'Resources'
    directory. If the 'Resources' directory is present in the current working
    directory, the path is constructed accordingly. If not, it looks for the
    'Resources' directory in the parent directory.

    Parameters:
    - file (str): The name of the file.

    Returns:
    - str: The full path for the specified file.
    """
    current_path = os.getcwd()

    # Check if 'Resources' directory exists in the current working directory
    if os.path.exists(os.path.join(current_path, "Resources")):
        _PATH = os.path.join(current_path, "Resources", file)
    else:
        # If 'Resources' directory is not in the current working directory,
        # look for it in the parent directory
        parent_path = os.path.dirname(current_path)
        if os.path.exists(os.path.join(parent_path, "Resources")):
            _PATH = os.path.join(parent_path, "Resources", file)
            
    return _PATH

def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points in 3D space.

    Parameters:
    - point1: NumPy array containing (x, y, z) coordinates of the first point.
    - point2: NumPy array containing (x, y, z) coordinates of the second point.

    Returns:
    - distance: Euclidean distance between the two points.
    """
    # Calculate the Euclidean distance
    distance = np.linalg.norm(point2 - point1)
    
    return distance

def generate_point(p):
    """
    Generate a random point in 3D space around a given point.

    This function generates a random point in 3D space around the specified point
    'p'. The point is randomly positioned within a spherical region of radius 0.1.

    Parameters:
    - p (list or ndarray): The coordinates of the center point in 3D space.

    Returns:
    - list: A list containing the x, y, and z coordinates of the generated point.
    """
    radius = 0.1#np.random.uniform(0, 1)

    # Generate random spherical coordinates
    theta = np.random.uniform(0, 2 * np.pi)
    phi = np.random.uniform(0, np.pi)

    # Convert spherical coordinates to Cartesian coordinates
    x = p[0] + radius * np.sin(phi) * np.cos(theta)
    y = p[1] + radius * np.sin(phi) * np.sin(theta)
    z = p[2] + radius * np.cos(phi)

    return [x, y, z]

def update_obj(box: CollisionShape, pos: list):
    """
    Update the position of a CollisionShape object.

    This function updates the position of a given CollisionShape object, 'box',
    by applying a rotation and translation based on the specified position.

    Parameters:
    - box (CollisionShape): The CollisionShape object to be updated.
    - pos (list): A list containing the x, y, and z coordinates of the new position.

    Returns:
    - None: The function updates the position of the CollisionShape object in-place.
    """
    axis = SO3.Rx(0) @ SO3.Ry(0)
    box.T = SE3.Rt(axis, pos)

def setup_env(**kwargs):
    """
    Set up a Swift environment with specified objects.

    This function sets up a Swift environment with various objects, including a start
    sphere, a destination sphere, cuboid boxes, and a Panda robot. The objects are
    positioned and colored based on the provided keyword arguments.

    Parameters:
    - **kwargs: Keyword arguments to customize the environment setup. Possible keys include:
        - "start": Boolean indicating whether to include a start sphere.
        - "dest": Boolean indicating whether to include a destination sphere.
        - "boxes": Boolean indicating whether to include cuboid boxes.
        - "panda": Boolean indicating whether to include a Panda robot.
        - "resources": Dictionary containing additional information for object customization.

    Returns:
    - tuple: A tuple containing a dictionary of created objects and the Swift environment.
    """
    env = swift.Swift()
    env.launch(realtime=True)

    objects = {}
    
    if "start" in kwargs and "resources" in kwargs and kwargs["start"]:
        start = Sphere(radius=kwargs["resources"]["radius"], color=kwargs["resources"]["start_color"])
        update_obj(start, kwargs["resources"]["start_loc"])
        objects["start"] = start
        env.add(start)
    if "dest" in kwargs and "resources" in kwargs and kwargs["dest"]:
        dest = Sphere(radius=kwargs["resources"]["radius"], color=kwargs["resources"]["dest_color"])
        update_obj(dest, kwargs["resources"]["dest_loc"])
        objects["dest"] = dest
        env.add(dest)
    if "boxes" in kwargs and "resources" in kwargs and kwargs["boxes"]:
        box = [Cuboid(scale=_scale, collision = True, color=(255, 10, 10)) for _scale in kwargs["resources"]["box_info"][:,0:3]/10]
        pos = [[_xyz[0], _xyz[1], _xyz[2]] for i, _xyz in enumerate(kwargs["resources"]["box_info"][:,3:6]) ]
        for i,_ in enumerate(box):
            update_obj(box[i], pos[i])
            env.add(box[i])
            pass
        objects["box"] = box
    if "panda" in kwargs and kwargs["panda"]:
        panda = rtb.models.Panda()
        panda.q = panda.qr
        env.add(panda)
        objects["panda"] = panda

    return objects, env

def generate_csv(filename, **kwargs):
    """
    Generate a CSV file with customizable content.

    This function creates a CSV file with the specified filename and content based
    on the provided keyword arguments. The content can include headers, random data,
    or an array of values.

    Parameters:
    - filename (str): The name of the CSV file to be generated.

    Keyword Arguments:
    - headers (list, optional): A list of headers for the CSV file.
    - random (int, optional): The number of rows of random data to generate.
    - limits (list, optional): A list of tuples specifying the limits for random data generation.
    - array (list, optional): A list of objects to be written to the CSV file.

    Returns:
    - None: The function writes the generated data directly to the specified CSV file.
    """
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if "headers" in kwargs:
            csv_writer.writerow(kwargs['headers'])

        if "random" in kwargs and "limits" in kwargs and kwargs["random"] > 0:
            for _ in range(kwargs['random']):
                row = [random.uniform(kwargs['limits'][index][0], kwargs['limits'][index][1]) for index, _ in enumerate(kwargs['limits'])]
                csv_writer.writerow(row)
        if "array" in kwargs:
            for index, object in enumerate(kwargs['array']):
                x = object[0]
                y = object[1]
                z = object[2]

                row = [x, y, z]
                csv_writer.writerow(row)

def generate_random_locs(amount: int):
    """
    Generate random locations in 3D space.

    This function generates a specified number of random locations in 3D space.
    The locations are represented as a NumPy array where each row corresponds to
    a location with x, y, and z coordinates.

    Parameters:
    - amount (int): The number of random locations to generate.

    Returns:
    - ndarray: A NumPy array containing random locations in 3D space.
    """
    rand = np.empty([amount,3])
    for i in range(amount):
        rand[i] = [random.uniform(-0.5, 0)*_ for _ in np.ones(3)]
    return rand

def robot_move(robot: rtb.models, env: swift.Swift, points: list):
    """
    Move a robot to a series of specified points in Cartesian space.

    This function controls the movement of a robot to a sequence of specified points
    in Cartesian space. The robot uses a proportional control scheme to adjust its
    joint velocities and reach the desired positions.

    Parameters:
    - robot (rtb.models): The roboticstoolbox robot model.
    - env (swift.Swift): The Swift environment for robot simulation.
    - points (list): A list of 3D points representing the desired end-effector positions.

    Returns:
    - None: The function controls the robot's movement in the specified environment.
    """
    Tep = robot.fkine(robot.q)
    Tep = robot.ikine_LM(Tep)
    dt = 0.05

    arrived = False

    for _,i in enumerate(points):
        while not arrived:
            v, arrived = rtb.p_servo(robot.fkine(robot.q), SE3.Rt(SO3.Rx(3.14)@SO3.Ry(0.0),i), 1)
            robot.qd = np.linalg.pinv(robot.jacobe(robot.q)) @ v
            env.step(dt)
        arrived = False
