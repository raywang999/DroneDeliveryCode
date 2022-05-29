import pygame
import json
import math

from typing import NewType
from drone_controller import drone_controller
from button import button

Coordinate = NewType('Coordinate', tuple[float, float])

def getDistance(coord1: Coordinate, coord2: Coordinate):
	cx, cy = coord1
	nx, ny = coord2
	return math.sqrt((cx-nx)*(cx-nx)+(cy-ny)*(cy-ny)) 

from heapq import heappush, heappop


pygame.init()
screen = pygame.display.set_mode([1500,720])
screen.fill((255,255,255))
running = True

# Need to measure the distance in px on map and the correspondence distance in real life in order
# to get coefficient

# For example: a px = b cm --> MAP_SIZE_COEFF = b/a

# 47px = 500cm --> MAP_SIZE_COEFF = 500/47
MAP_SIZE_COEFF = 500/136

class Background(pygame.sprite.Sprite):
    def __init__(self, image, location, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def get_dist(pos0, pos1):

    # Get the distance between 2 positions (or 2 points)

    dis_px = math.sqrt((pos1[0]-pos0[0])**2 + (pos1[1]-pos0[1])**2)
    dis_cm = dis_px*MAP_SIZE_COEFF
    return int(dis_cm), int(dis_px)

# input: starting Coordinate, an array of Coordinates representing desired destinations, ending destination
# output: an array of Coordinates listed in order of travel for shortest travel distances
def shortestPath(start: Coordinate, stops: list[Coordinate], end: Coordinate):
	itocoord: dict[int, Coordinate] = {0: start, 1: end}
	itostops: dict[int, Coordinate] = {}
	for stop in stops:
		itocoord[len(itocoord)]=stop
		itostops[len(itostops)+2]=stop
	pq: list[tuple[int, list[int]]] = []
	heappush(pq, (0, [0]))
	minTime = 1000*60*60 # one hour
	resultPath = []
	while (len(pq)>0):
		time, path = heappop(pq)
		nextStops = {} 
		for i in range(2, len(stops)+2):
			nextStops[i] = True
		for visStop in path:
			nextStops.pop(visStop, None)
		currCoord = itocoord[path[len(path)-1]]
		if (len(nextStops)==0):
			if (time>minTime): break
			time += get_dist(currCoord, end)[0]
			path.append(1) # Add end coordinate to path
			if (time<minTime):
				minTime=time
				resultPath=path
		for nextStop in nextStops:
			newpath = path.copy()
			newpath.append(nextStop)
			heappush(pq, (time+ get_dist(currCoord, itocoord[nextStop])[0], newpath))
	return list(map(lambda i: itocoord[i], resultPath))
		
def get_turning_angle(pos0, pos1, posref):
    # Get the angle between 2 lines relative to "posref"
    # Did so by using dot product calculation

    # we need 3 points to run this function, and the middle waypoint is "posref"

    # magnitude of A
    aX = posref[0]-pos0[0]
    aY = posref[1]-pos0[1]
    magA = math.sqrt(aX**2 + aY**2)

    # magnitude of B
    bX = posref[0]-pos1[0]
    bY = posref[1]-pos1[1]
    magB = math.sqrt(bX**2 + bY**2)

    #  dot product
    _dot = (aX*bX)+(aY*bY)

    # spit out the angle

    turning_angle_rad = math.acos(_dot/(magA*magB))

    # convert to degrees, as acos() return the answer in radians

    return int((turning_angle_rad*180)/math.pi)



# List of last waypoints and the current waypoint to draw path
path_wp = []

# Pointer
index = 0

def save_JSON():
    global path_wp
    # Computing waypoints (distance and angle)

    path_dis_cm=[]
    path_dis_px =[]
    path_angle = []

    # print('path_wp (before): ', format(path_wp))


    path_wp = shortestPath(path_wp[0], path_wp[1:len(path_wp)-1], path_wp[len(path_wp)-1])

    # Append first pos ref. (this is a dummy) to help the drone navigate where to go after taking off
    path_wp.insert(0, (path_wp[0][0], path_wp[0][1] - 10))

    for index in range(len(path_wp)):
        # Skip first and second index (dummy)
        if(index > 1):
            dis_cm, dis_px = get_dist(path_wp[index-1], path_wp[index])
            path_dis_cm.append(dis_cm)
            path_dis_px.append(dis_px)
        
        if index > 0 and index < len(path_wp)-1:
            # skip first and last index as we don't have enough info
            angle = get_turning_angle(path_wp[index -1], path_wp[index+1], path_wp[index])
            path_angle.append(angle) 

    print('path_wp (after): ', format(path_wp))
    # print('dis_cm: {}', format(path_dis_cm))
    # print('dis_px: {}', format(path_dis_px))
    # print('dis_angle: {}', format(path_angle))

    # Save waypoints in JSON file

    waypoints = []

    for i in range (len(path_dis_cm)):
        waypoints.append({
            "dist_cm": path_dis_cm[i],
            "dis_px": path_dis_px[i],
            "angle_deg": path_angle[i]
        })

    #  Save JSON file

    f = open('waypoints.json', 'w+')
    path_wp.pop(0) #Remove the dummy before saving
    json.dump({
        "wp": waypoints,
        "pos": path_wp
    }, f, indent = 4)
    f.close()

# load background image
bg = Background('image.png', [0,0], 0.8)
screen.blit(bg.image, bg.rect)

take_off = button((0, 255, 0), 1260, 260, 150, 100, 'Take-Off')
plan_path = button((0, 255, 0), 1260, 460, 150, 100, 'Plan Path')

# Get mouse input => Set waypoints
while running:
    for event in pygame.event.get():
        take_off.draw(screen, (0,0,0))
        plan_path.draw(screen, (0, 0 ,0))
            
        if event.type == pygame.QUIT:
            # Quit the program when the "X" button is clicked
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position where the mouse click is
            pos = pygame.mouse.get_pos()

            
            if pos[0] <1180:
                # print("Less than 1100")
                # Add position where we just clicked
                path_wp.append(pos)
                index += 1 
                pygame.draw.circle(screen, (255, 0,0 ), pos, 5)
            

            if(take_off.isOver(pos)):
                save_JSON()
                d = drone_controller()
                d.main_controller()
            
            if(plan_path.isOver(pos)):
                for i in range (0, len(path_wp)-1):
                    pygame.draw.line(screen, (255, 0, 0), path_wp[i], path_wp[i+1], 2)
                


            # if index > 0:
                # pygame.draw.line(screen, (255,0,0), path_wp[index-1], pos, 2)
            


    pygame.display.update()


