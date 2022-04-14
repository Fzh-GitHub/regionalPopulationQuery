from types import CellType
from sanic import Sanic
from sanic import response
from sanic.response import json
from shapely import geometry
from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt
import json

app = Sanic(__name__)

xlist = list()
ylist = list()
colorList = list()

def calcPopulation(lonLats):
    lonMin = 999
    latMin = 999
    lonMax = -999
    latMax = -999
    polygon = geometry.Polygon(lonLats)
    lonMin,latMin,lonMax,latMax = polygon.bounds
    step = 5/6
    lonMin = lonMin - lonMin%step + step
    lonMax = lonMax - lonMax%step
    latMin = latMin - latMin%step + step
    latMax = latMax - latMax%step
    step = 5
    populationTotal = 0
    for lon in np.arange(lonMin,lonMax,step):
        for lat in np.arange(latMin,latMax,step):
            PSW = (lon , lat)
            PSE = (lon + step , lat)
            PNW = (lon, lat + step)
            PNE = (lon + step,lat + step)
            lonLatsofSquare = [PSW,PSE,PNW,PNE]
            cellPolygon = geometry.Polygon(lonLatsofSquare)
            if polygon.contains(cellPolygon) == True:
                population = getPopulationFromFile(lonLatsofSquare)
                if float(population) != -9999:
                    populationTotal += float(population)*36
                xlist.append((lon+lon+step)/2)
                ylist.append((lat+lat+step)/2)
                if float(population) > 3000:
                    colorList.append('red')
                elif float(population) > 1000:
                    colorList.append('orange')
                elif float(population) > 500:
                    colorList.append('yellow')
                elif float(population) > 100:
                    colorList.append('green')
                elif float(population) > 50:
                    colorList.append('greenyellow')
                elif float(population) > 10:
                    colorList.append('cyan')
                elif float(population) != -9999:
                    colorList.append('skyblue')
                else:
                    colorList.append('blue')
    with open('Polygon.json','r') as file:
        line = file.read()
        dict = {'total' : populationTotal,'xlist':xlist,'ylist':ylist,'color':colorList,'polygon':line}
    global json_str 
    json_str = json.dumps(dict)
    
@app.route('/json')
async def handle_request(request):
    pointList = list()
    with open('polygon.json') as file:
        polygonJson = file.read()
        jsonDict = eval(polygonJson)
        for i in range(0,len(jsonDict['coordinates'][0])):
            pointList.append(jsonDict['coordinates'][0][i])     
    calcPopulation(pointList)
    with open('population.json','w') as f:
        f.write(json_str)
    f.close()
    return await response.file('population.json')

def getPopulationFromFile(square):
    temp = 0
    step = 5/6
    cols = int( ( 180 + square[2][0] ) / step )
    lines = int( ( 90 - square[2][1] ) / step )
    with open('final.txt','r') as file:
        tempIndex = 0
        flag = 0
        line = file.readline()
        while tempIndex < lines + 6:
            line = file.readline()
            if tempIndex >= lines:
                popList = line.split(' ')
                for i in range(cols,cols + 6):
                    if float(popList[i]) != -9999:
                        temp += float(popList[i])       
                        flag = 1 
            tempIndex = tempIndex + 1
    file.close()
    if flag == 1:
        return temp/36
    else:
        return -9999

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)

