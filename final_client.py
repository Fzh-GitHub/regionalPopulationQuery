import aiohttp
import asyncio
import json
import xml.etree.ElementTree as xmlet
import matplotlib.pyplot as plt
from shapely import geometry
from shapely.geometry import Polygon
import argparse
import logging

pointList = list()

async def main(host,port,fmt):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://{host}:{port}/{fmt}') as response:
            logger.info("Start processing answer...")
            print("Content-type:", response.headers['content-type'])
            aDict = dict()
            html = await response.text()
            if fmt =='json':
                aDict = json.loads(html)
                totalPopulation = aDict['total']
                logger.info("Total population is "+str(totalPopulation))
                xlist = aDict['xlist']
                ylist = aDict['ylist']
                colorList = aDict['color']
                jsonPolygon = aDict['polygon']
                jsonDict = eval(str(jsonPolygon))
                for i in range(0,len(jsonDict['coordinates'][0])):
                    pointList.append(jsonDict['coordinates'][0][i]) 
                logger.info("Query range is "+str(pointList))             
                plt.scatter(xlist,ylist,c=colorList)
                polygon1 = Polygon(pointList)
                x,y = polygon1.exterior.xy
                plt.plot(x,y,linewidth = '1',color = 'black')
                plt.xlim(-180, 180)
                plt.ylim(-90, 90)
                plt.xlabel('longitude', horizontalalignment='right', x=1.0) 
                plt.ylabel('latitude',horizontalalignment='right', y=1.0)
                ax = plt.gca()    # 得到图像的Axes对象
                ax.spines['right'].set_color('none')   # 将图像右边的轴设为透明
                ax.spines['top'].set_color('none')     # 将图像上面的轴设为透明
                ax.xaxis.set_ticks_position('bottom')    # 将x轴刻度设在下面的坐标轴上
                ax.yaxis.set_ticks_position('left')         # 将y轴刻度设在左边的坐标轴上
                ax.spines['bottom'].set_position(('data', 0))   # 将两个坐标轴的位置设在数据点原点
                ax.spines['left'].set_position(('data', 0))
                type1 = plt.scatter([-200],[-200],s=20, c='red')
                type2 = plt.scatter([-200],[-200],s=20, c='orange')
                type3 = plt.scatter([-200],[-200],s=20, c='yellow')
                type4 = plt.scatter([-200],[-200],s=20, c='green')
                type5 = plt.scatter([-200],[-200],s=20, c='greenyellow')
                type6 = plt.scatter([-200],[-200],s=20, c='cyan')
                type7 = plt.scatter([-200],[-200],s=20, c='skyblue')
                type8 = plt.scatter([-200],[-200],s=20, c='blue')
                plt.legend((type1,type2,type3,type4,type5,type6,type7,type8), ('>3000','>1000','>500','>100','>50','>10','>=0','no data'), loc=2)
                plt.title('World population distribution')
                plt.show()
                logger.info("Finish")
            
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler("log.log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    parser = argparse.ArgumentParser(description='world temperature client')
    parser.add_argument('--fmt',dest='fmt',default='json')
    parser.add_argument('host')
    parser.add_argument('port')
    args = parser.parse_args()
    print(f'{args}')
    asyncio.run(main(args.host,args.port,args.fmt))    