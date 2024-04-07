import math 
import os
import operator
import sys

# 12 * 60
MAX_TIME = 720

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def dataToPoint(data):
	s = data.replace("(","").replace(")","").split(",")
	return Point(float(s[0]), float(s[1]))
	
def calcDistance(x1, x2, y1, y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1) **2)

def calcDistanceTwoPoints(p1, p2):
	return calcDistance(p1.x, p2.x, p1.y, p2.y)

totalTrips = {}
with open(sys.argv[1]) as f:
	next(f)
	for line in f:
		line = line.replace("\n", "")
		data = line.split(" ")
		route = data[0]

		pickup = dataToPoint(data[1])
		dropoff = dataToPoint(data[2])
		origin = Point(0, 0)

		euc = calcDistanceTwoPoints(pickup, dropoff)
		distPickup = calcDistanceTwoPoints(origin, pickup)
		distReturn = calcDistanceTwoPoints(dropoff, origin)

		totalTrips[route] = euc + distPickup + distReturn

	# naive solution 
	# This solution has all the drivers returning to and from the depot after every trip 
	# and we optimize the driver schedule based on how many overall trips we can fit in 
	# between the max allotted time (12*60)
	# NOTE this is bad this is just a base case to set everything up to work

	totalTrips = sorted(totalTrips.items(), key=operator.itemgetter(1))
	routes = []
	distance = 0
	for trip in totalTrips:
		route = trip[0]
		tripDist = float(trip[1])
		if distance + tripDist < MAX_TIME:
			distance += tripDist
			routes.append(route)
		else:
			sys.stdout.write("[" + ",".join(routes) + "]\n")
			routes.clear()
			routes.append(route)
			distance = tripDist

	sys.stdout.write("[" + ",".join(routes) + "]\n")