'''
This class is used to read the JSON file and control the drone's movements
'''

import json
from djitellopy import tello

drone = tello.Tello()

path_coords = []
path_dist = []
turning_angle = []

class drone_controller:

    def __init__(self):
        f = open('waypoints.json', "r")
        data = json.loads(f.read())    
        for i in data["pos"]:
            path_coords.append(i)

        for i in data["wp"]:
            path_dist.append(i["dist_cm"])
    
        for i in data["wp"]:
            turning_angle.append(i["angle_deg"])
        
    def turn_left(deg):
        drone.rotate_counter_clockwise(180-deg)

    def turn_right(deg):
        drone.rotate_clockwise(180-deg)
    
d = drone_controller()

print("length path_coords: ", len(path_coords))
print("length path_dist: ", len(path_dist))s
print(turning_angle)

# loop through the coordinate points and adjust the drone's direction accordingly
for i in range (1,len(path_coords)+1):
    if path_coords[i][0] > path_coords[i-1][0]:
        d.turn_right(turning_angle[i-1])
    else:
        d.turn_left(turning_angle[i-1])
    
    drone.move_forward(path_dist[i-1])

drone.land()




