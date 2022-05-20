from math import sqrt
from typing import NewType

Coordinate = NewType('Coordinate', tuple[float, float])

def getDistance(coord1: Coordinate, coord2: Coordinate):
	cx, cy = coord1
	nx, ny = coord2
	return sqrt((cx-nx)*(cx-nx)+(cy-ny)*(cy-ny)) 

# input: starting Coordinate, an array of Coordinates representing desired destinations, ending destination
# output: an array of Coordinates listed in order of travel for shortest travel distances
from heapq import heappush, heappop

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
			time += getDistance(currCoord, end)
			path.append(1) # Add end coordinate to path
			if (time<minTime):
				minTime=time
				resultPath=path
		for nextStop in nextStops:
			newpath = path.copy()
			newpath.append(nextStop)
			heappush(pq, (time+getDistance(currCoord, itocoord[nextStop]), newpath))
	return list(map(lambda i: itocoord[i], resultPath))
		