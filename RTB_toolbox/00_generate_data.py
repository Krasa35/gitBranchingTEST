import lib.callbacks as call
import random

limits_dict =   {"box_size":    [5/2,   7/2],
                "x":            [-0.7,  0.7],
                "y":            [-0.7,  0.7],
                "z":            [-1.0,  0.8]}

limits = [limits_dict['box_size'],
          limits_dict['box_size'],
          limits_dict['box_size'],
          limits_dict['x'],
          limits_dict['y'],
          limits_dict['z']] 

if __name__ == "__main__":
    PATH = call.handle_path("restricted_area.csv")
    headers = ['scale_x', 'scale_y', 'scale_z', 'pos_x', 'pos_y', 'pos_z']

    call.generate_csv(PATH, headers= headers, random=15, limits=limits)