import pandas
from spatialgeometry import Sphere
import numpy as np
import lib.callbacks as call

#PATH = call.handle_path("restricted_area.csv")
PATH = call.handle_path("restricted_area.csv")
df = pandas.read_csv(PATH)

limits = [[-0.4, 0.4], [-0.6, 0.6], [0.0, 0.7]]
resources = {"radius":                  0.04,
             "point_to_check_color":    (0, 0, 0),
             "map_limits":              [-2, 2, -2, 2,-1, 3],
             "start_loc":               [np.random.uniform(limits[index][0], limits[index][1]) for index, _ in enumerate(limits)],
             "start_color":             (0, 255, 0),
             "dest_color":              (0, 0, 255),
             "dest_loc":                [np.random.uniform(limits[index][0], limits[index][1]) for index,_ in enumerate(limits)],
             "iterations":              10,
             "box_info":                df.values}

objects, env = call.setup_env(start=True, 
                              dest = True, 
                              boxes = True,
                              resources = resources)

current = Sphere(radius=resources["radius"], color=(255,255,0))

Togo = [objects['start']]
Togo_list = [np.array(objects['start'].T[0:3,3])]
Temp = objects['start']
cnt = 0
in_collision = False

while True:
    for i in range(resources["iterations"]):
        best_pose = Togo[cnt].T[0:3,3]
        center = call.generate_point(best_pose)
        current = Sphere(radius=resources["radius"], color=(10,10,10))
        call.update_obj(current, center)
        for instance_box in objects["box"]:
            if current.iscollided(instance_box) == True:
                in_collision = True
                break
            else:
                in_collision = False
        env.add(current)
        if (call.euclidean_distance(current.T[0:3,3], objects['dest'].T[0:3,3]) < call.euclidean_distance(Temp.T[0:3,3], objects['dest'].T[0:3,3])) and not in_collision:
            if Temp!=objects['start']:
                env.remove(Temp)
            Temp = current
            if objects['dest'].iscollided(Temp):
                break
        else:
            env.remove(current)
    cnt += 1
    Togo.append(Temp)
    Togo_list.append(np.array(Temp.T[0:3,3]))
    env.add(Togo[-1])
    if objects['dest'].iscollided(Temp):
        headers = ['x', 'y', 'z']
        PATH = call.handle_path("points.csv")
        call.generate_csv(PATH, headers=headers, array=Togo_list)
        break
print(f"The point has arrived to its destination with {cnt} itterations")
