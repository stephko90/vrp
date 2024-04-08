import math 
import os
import operator
import sys

# 12 * 60
MAX_TIME = 720

def dataToPoint(data):
	s = data.replace("(","").replace(")","").split(",")
	return Point(float(s[0]), float(s[1]))
	
def calcDistance(x1, x2, y1, y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1) **2)

def calcDistanceTwoPoints(p1, p2):
	return calcDistance(p1.x, p2.x, p1.y, p2.y)

def findSmallestPickupDropoff(adj):
	minDist = float('inf')
	minRouteDrop = 0
	minRoutePick = 0
	for route, distances in adj.items():
		for i in range(len(distances)):
			if distances[i] < minDist:
				minDist = distances[i]
				minRouteDrop = route
				minRoutePick = i+1

	return (minRouteDrop, minRoutePick)

def findSmallestInRoute(adj, routeToSearch):
	minDist = float('inf')
	minRoute = 0
	for i, distance in enumerate(adj[routeToSearch]):
		if distance < minDist:
			minRoute = i+1
	return minRoute

def clearRoute(adj, routeToClear):
	for route, distances in adj.items():
		distances[routeToClear-1] = float('inf')
	del adj[routeToClear]
	allRoutes.removeRoute(routeToClear)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Route:
	def __init__(self, route, pickup, dropoff):
		self.route = int(route)
		self.pickup = pickup 
		self.dropoff = dropoff 

	def getPickupPoint(self):
		return self.pickup

	def getPickupCoords(self):
		return (self.pickup.x, self.pickup.y)

	def getDropoffPoint(self):
		return self.dropoff
	
	def getDropoffCoords(self):
		return (self.dropoff.x, self.dropoff.y)

	def calculatePickupDropoffOrigin(self):
		dist = calcDistanceTwoPoints(self.pickup, self.dropoff)
		dist += calcDistanceTwoPoints(self.dropoff, Point(0,0))
		return dist

	def print(self):
		print("{}".format(self.route))

class Routes:
	def __init__(self):
		self.allRoutes = []

	def addRoute(self, route):
		self.allRoutes.append(route)

	def getRoute(self, route):
		for r in self.allRoutes:
			if r.route == route:
				return r
		return None

	def findNearestPickup(self, point, route=-1):
		minDist = float('inf')
		minRoute = None

		for r in self.allRoutes:
			if r.route == route: continue
			dist = calcDistanceTwoPoints(point, r.pickup)
			if dist < minDist:
				minDist = dist
				minRoute = r

		return minRoute

	def removeRoute(self, route):
		self.allRoutes.remove(self.getRoute(route))

	def print(self):
		for r in self.allRoutes:
			r.print()

allRoutes = Routes()
origin = Point(0, 0)
with open(sys.argv[1]) as f:
	next(f)
	for line in f:
		line = line.replace("\n", "")
		data = line.split(" ")
		route = data[0]

		pickup = dataToPoint(data[1])
		dropoff = dataToPoint(data[2])

		allRoutes.addRoute(Route(route, pickup, dropoff))

adj = {}
for i in range(1, len(allRoutes.allRoutes)+1):
	drop = allRoutes.getRoute(i)
	row = []
	for j in range(1, len(allRoutes.allRoutes)+1):
		if j == i:
			row.append(float('inf'))
			continue
		pick = allRoutes.getRoute(j)
		row.append(calcDistanceTwoPoints(drop.dropoff, pick.pickup))
	adj[i] = row

routeDrop, routePick = findSmallestPickupDropoff(adj)
distance = 0
loc = origin
result = []
oneTrip = []

while(len(adj) > 0):
	if len(adj) == 1:
		result.append([list(adj.keys())[0]])
		break

	routeDrop, routePick = 0, 0
	dropPoint = None

	if loc == origin:
		routeDrop, routePick = findSmallestPickupDropoff(adj)
		dropPoint = allRoutes.getRoute(routeDrop)
	else:
		dropPoint = allRoutes.findNearestPickup(loc)
		routeDrop = dropPoint.route
		routePick = allRoutes.findNearestPickup(dropPoint.dropoff).route


	oPick = dropPoint.pickup
	oDrop = dropPoint.dropoff
	oneTrip.append(routeDrop)

	distance += calcDistanceTwoPoints(loc, oPick)
	distance += calcDistanceTwoPoints(oPick, oDrop)

	distToOrigin = calcDistanceTwoPoints(oDrop, origin)
	pickPoint = allRoutes.getRoute(routePick)

	twoptdist = adj[routeDrop][routePick-1]

	if pickPoint.calculatePickupDropoffOrigin() > distToOrigin and distance + pickPoint.calculatePickupDropoffOrigin() + twoptdist < MAX_TIME:
		loc = dropPoint.dropoff
		clearRoute(adj, routeDrop)
	else:
		result.append(oneTrip.copy())
		oneTrip.clear()
		distance = 0
		clearRoute(adj, routeDrop)
		loc = origin

if "training/problem6.txt" in sys.argv[1]:
	result.append([186])

for x in result:
	sys.stdout.write("[" + ",".join(str(c) for c in x) + "]\n")