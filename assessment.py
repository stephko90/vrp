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
with open(sys.argv[1]) as f:
	next(f)
	for line in f:
		line = line.replace("\n", "")
		data = line.split(" ")
		route = data[0]

		pickup = dataToPoint(data[1])
		dropoff = dataToPoint(data[2])

		allRoutes.addRoute(Route(route, pickup, dropoff))

"""
	Better solution that takes a greedy nextdoor neighbor approach when choosing whether to move to the next closes node in the plane or return to the origin
	An optimization - while the selection of the node mid route has some logic, the selection of the node from the origin only takes distance
	into account. Instead we can try and find a solution that optimization origin node selection
	NOTE: The pass again logic is NOT something that I would merge into production code in it's current state, it's more of an idea to whittle down the total cost
"""
origin = Point(0, 0)
distance = 0
loc = origin
result = []
oneTrip = []
passAgain = Routes()
while(len(allRoutes.allRoutes) > 0):
	nearestFromOrigin = allRoutes.findNearestPickup(loc)
	oRoute = nearestFromOrigin.route
	oPick = nearestFromOrigin.pickup
	oDrop = nearestFromOrigin.dropoff
	oneTrip.append(oRoute)

	distance += calcDistanceTwoPoints(loc, oPick)
	distance += calcDistanceTwoPoints(oPick, oDrop)

	distToOrigin = calcDistanceTwoPoints(oDrop, origin)
	nearestPickup = allRoutes.findNearestPickup(oDrop, oRoute)
	if nearestPickup is None:
		if len(oneTrip) == 1: 
			passAgain.addRoute(Route(oRoute, oPick, oDrop))
		else:
			result.append(oneTrip.copy())
		break

	distNearestPickup = calcDistanceTwoPoints(oDrop, nearestPickup.pickup)

	# if the total cost to complete another route is greater than the cost to return to the depot 
	# AND the cost of the trip with the current distance is less than the max time allotted
	if nearestPickup.calculatePickupDropoffOrigin() > distToOrigin and distance + nearestPickup.calculatePickupDropoffOrigin() + distNearestPickup < MAX_TIME:
		loc = oDrop
		allRoutes.removeRoute(oRoute)
	else:
		if len(oneTrip) == 1: 
			passAgain.addRoute(Route(oRoute, oPick, oDrop))
		else:
			result.append(oneTrip.copy())
		oneTrip.clear()
		distance = 0
		allRoutes.removeRoute(oRoute)
		loc = origin


# I'm not a huge fan of this block of logic here and since I don't have time to implement this idea fully, here is my thought process:
# the above block of code would get moved into a function. we then continue to iterate over the remainders of the single nodes until
# it is mathematically impossible to create more connections. The idea being that drivers cost vastly more so we want to be sure that
# we've created as many edges as possible between all the nodes that we can
loc = origin
distance = 0
oneTrip.clear()
while(len(passAgain.allRoutes) > 0):
	nearestFromOrigin = passAgain.findNearestPickup(loc)
	oRoute = nearestFromOrigin.route
	oPick = nearestFromOrigin.pickup
	oDrop = nearestFromOrigin.dropoff
	oneTrip.append(oRoute)

	distance += calcDistanceTwoPoints(loc, oPick)
	distance += calcDistanceTwoPoints(oPick, oDrop)

	distOrigin = calcDistanceTwoPoints(oDrop, origin)
	nearestPickup = passAgain.findNearestPickup(oDrop, oRoute)
	
	if nearestPickup is None:
		result.append(oneTrip.copy())
		break

	distNearestPickup = calcDistanceTwoPoints(oDrop, nearestPickup.pickup)

	if nearestPickup.calculatePickupDropoffOrigin() > distOrigin and distance + nearestPickup.calculatePickupDropoffOrigin() + distNearestPickup < MAX_TIME:
		loc = oDrop
		passAgain.removeRoute(oRoute)
			
	else:
		result.append(oneTrip.copy())
		oneTrip.clear()
		distance = 0
		passAgain.removeRoute(oRoute)
		loc = origin
			
for x in result:
	sys.stdout.write("[" + ",".join(str(c) for c in x) + "]\n")