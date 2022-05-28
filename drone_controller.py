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
        
    def turn_left(self, value, deg):
        if value == 0:
            # print("left: ", deg)
            drone.rotate_counter_clockwise(deg)

        
        else:
            # print("left: ", 180 - deg)
            drone.rotate_counter_clockwise(180-deg)


    def turn_right(self, value, deg):
        if(value == 0):
            # print("right: ", deg)
            drone.rotate_clockwise(deg)

        else:
            # print("right: ", 180-deg)
            drone.rotate_clockwise(180-deg)


    
    def main_controller(self):
        drone.takeoff()

        

        # loop through the coordinate points and adjust the drone's direction accordingly
        for i in range (1,len(path_coords)):
            
            if path_coords[i][0] > path_coords[i-1][0]:
                    self.turn_right(i-1,turning_angle[i-1])   
            else:
                self.turn_left(i-1, turning_angle[i-1])

            drone.move_forward(path_dist[i-1])
            # print(turning_angle[i-1])

        drone.land()




# print("length path_coords: ", len(path_coords))
# print("length path_dist: ", len(path_dist))
# print(turning_angle)






