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

class Trips:
	def __init__(self):
		self.totalTrips = {}

	def add(self, route, distance):
		self.totalTrips[route] = distance

	def sortVals(self):
		self.totalTrips = sorted(self.totalTrips.items(), key=operator.itemgetter(1))

	def printTrips(self):
		print(self.totalTrips)

	def printFormatted(self):
		routes = []
		distance = 0
		totalDistance = 0
		drivers = 1
		for trip in self.totalTrips:
			route = trip[0]
			tripDist = float(trip[1])
			totalDistance += tripDist
			if distance + tripDist < MAX_TIME:
				distance += tripDist
				routes.append(route)
			else:
				drivers += 1
				sys.stdout.write("[" + ",".join(routes) + "]\n")
				routes.clear()
				routes.append(route)
				distance = tripDist

		sys.stdout.write("[" + ",".join(routes) + "]\n")
		totalCost = (500*drivers) + totalDistance
		print(totalCost)

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
trips = Trips()
tripsToPickup = Trips()
tripsToReturn = Trips()
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
		euc = calcDistanceTwoPoints(pickup, dropoff)
		distPickup = calcDistanceTwoPoints(origin, pickup)
		distReturn = calcDistanceTwoPoints(dropoff, origin)

		trips.add(route, euc)
		tripsToPickup.add(route, distPickup)
		tripsToReturn.add(route, distReturn)

	# naive solution 
	# This solution has all the drivers returning to and from the depot after every trip 
	# and we optimize the driver schedule based on how many overall trips we can fit in 
	# between the max allotted time (12*60)
	# NOTE this is bad this is just a base case to set everything up to work
print(allRoutes)
trips.sortVals()
tripsToPickup.sortVals()
tripsToReturn.sortVals()

trips.printTrips()
tripsToPickup.printTrips()
tripsToReturn.printTrips()

trips.printFormatted()

route1 = allRoutes.getRoute(1)
print(route1)
nearestPickup = allRoutes.findNearestPickup(route1.dropoff)
print(nearestPickup.route)

nearestFromOrigin = allRoutes.findNearestPickup(origin)
print(nearestFromOrigin.route)

distance = 0
loc = origin
result = []
oneTrip = []
while(len(allRoutes.allRoutes) > 0):
	nearestFromOrigin = allRoutes.findNearestPickup(loc)
	oneTrip.append(nearestFromOrigin.route)

	distance += calcDistanceTwoPoints(loc, nearestFromOrigin.pickup)
	distance += calcDistanceTwoPoints(nearestFromOrigin.pickup, nearestFromOrigin.dropoff)

	distOrigin = calcDistanceTwoPoints(nearestFromOrigin.dropoff, origin)
	nearestPickup = allRoutes.findNearestPickup(nearestFromOrigin.dropoff, nearestFromOrigin.route)
	if nearestPickup is None:
		result.append(oneTrip.copy())
		break

	distNearestPickup = calcDistanceTwoPoints(nearestFromOrigin.dropoff, nearestPickup.pickup)

	if nearestPickup.calculatePickupDropoffOrigin() > distOrigin and distance + nearestPickup.calculatePickupDropoffOrigin() + distNearestPickup < MAX_TIME:
		loc = nearestFromOrigin.dropoff
		allRoutes.removeRoute(nearestFromOrigin.route)
			
	else:
		result.append(oneTrip.copy())
		oneTrip.clear()
		distance = 0
		allRoutes.removeRoute(nearestFromOrigin.route)
		loc = origin
			
print(result)