'''
This class is used to read the JSON file and control the drone's movements
'''

import json
from djitellopy import tello

drone = tello.Tello()

class drone_controller:
    path_coords = []
    path_dist = []

    def __init__(self):
        f = open('waypoints.json', "r")
        data = json.loads(f.read())    
        for i in data["pos"]:
            self.path_coords.append(i)

        for i in data["wp"]:
            self.path_dist.append(i)
    
    def turn_left(deg):
        drone.rotate_counter_clockwise(180-deg)

    def turn_right(deg):
        drone.rotate_clockwise(180-deg)

    def get_path_coords():
        return path_coords

    def get_path_dist():
        return path_dist    
    


d = drone_controller()




