"""
Jacob Taylor
11/5/2015
Program1
Find all the cities within a bounding box and a certain radius using the code given
"""
import pyqtree
import csv
from math import *
from haversine import haversine
import numpy as np
import time

def loadCities():
    citys = []
    with open('citylist.csv', 'rb') as csvfile:
        citysCsv = csv.reader(csvfile, delimiter=',', quotechar='"')
        for city in citysCsv:
            citys.append({"Name":city[0],"Country":city[1],"lat":city[2],"lon":city[3]})
    return citys

def displace(lat,lng,theta, distance,unit="miles"):
    """
    Displace a LatLng theta degrees clockwise and some feet in that direction.
    Notes:
        http://www.movable-type.co.uk/scripts/latlong.html
        0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
    Args:
        theta:    A number in degrees where:
                  0   = North
                  90  = East
                  180 = South
                  270 = West
        distance: A number in specified unit.
        unit:     enum("miles","kilometers")
    Returns:
        A new LatLng.
    """
    theta = np.float32(theta)
    radiusInMiles = 3959
    radiusInKilometers = 6371

    if unit == "miles":
        radius = radiusInMiles
    else:
        radius = radiusInKilometers

    delta = np.divide(np.float32(distance), np.float32(radius))

    theta = deg2rad(theta)
    lat1 = deg2rad(lat)
    lng1 = deg2rad(lng)

    lat2 = np.arcsin( np.sin(lat1) * np.cos(delta) +
                      np.cos(lat1) * np.sin(delta) * np.cos(theta) )

    lng2 = lng1 + np.arctan2( np.sin(theta) * np.sin(delta) * np.cos(lat1),
                              np.cos(delta) - np.sin(lat1) * np.sin(lat2))

    lng2 = (lng2 + 3 * np.pi) % (2 * np.pi) - np.pi

    return [rad2deg(lat2), rad2deg(lng2)]

def deg2rad(theta):
        return np.divide(np.dot(theta, np.pi), np.float32(180.0))

def rad2deg(theta):
        return np.divide(np.dot(theta, np.float32(180.0)), np.pi)

def main():
    start_time = time.time()
    spindex = pyqtree.Index(bbox=[0,0,360,180])
    cities = loadCities()
    out = open('output.dat', 'w')
    out.write("Jacob Taylor \n10/22/2015 \nProgram 1 - Intro to Quadtrees\n")
    out.write("============================================================================================\n")
    out.write("1. All cities within the bounding box: [45.011419, -111.071777 , 40.996484, -104.040527]:\n\n")

    """
    Loops through all the cities and checks if they are within the given bounding box.
    If the city is withing the bounding box it is written to the file
    """
    for c in cities:
        #{'lat': '-18.01274', 'Country': 'Zimbabwe', 'lon': '31.07555', 'Name': 'Chitungwiza'}
        item = c['Name']

        minLat = float(c['lat'])-.1
        minLon = float(c['lon'])-.1
        maxLat = float(c['lat'])+.1
        maxLon = float(c['lon'])+.1

        bbox =[minLat,minLon,maxLat,maxLon]

        spindex.insert(item=item, bbox=bbox)

    """overlapbbox = (51,51,86,86)"""
    overlapbbox = (45.011419, -111.071777 , 40.996484, -104.040527)
    matches = spindex.intersect(overlapbbox)

    out.write("\n".join(str(x) for x in matches))
    out.write("\n============================================================================================\n")
    out.write("2. All cities within 500 miles of this point: (23.805450, -78.156738):\n")

    """
    Loops through all the cities in the csv file and compares their ditance from a given point
    If the distance is within 500 miles the city is written out to the file
    """
    for c in cities:
        lat1 = float(c['lat'])
        lon1 = float(c['lon'])

        distance = haversine((lat1,lon1),(23.805450, -78.156738),miles = True)

        if distance <= 500:
            out.write("\n")
            out.write(c['Name'])
    out.write("\n============================================================================================\n")
    out.write("\nProgram ran in %s seconds." % (time.time() - start_time))
    out.close

if __name__ == '__main__':
    main()
