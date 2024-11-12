import pandas
import lib.callbacks as call

PATH = call.handle_path("restricted_area.csv")
df = pandas.read_csv(PATH)
PATH = call.handle_path("points.csv")
df_p = pandas.read_csv(PATH)

resources = {"start_loc":   df_p.values[0,:],
             "dest_loc":    df_p.values[-1,:],
             "radius":      0.04,
             "start_color": (0, 255, 0),
             "dest_color":  (0, 0, 255),
             "box_color":   (255, 10, 10),
             "box_info":    df.values,}

objects, env = call.setup_env(panda=True,
                              boxes = True, 
                              start = True, 
                              dest = True, 
                              resources=resources)  
call.robot_move(objects["panda"], env, df_p.values)    