# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 16:57:45 2018

@author: Anaëlle
"""

from lxml import etree

xmldoc = etree.parse("result_trump2.tcf.xml")

latitudes = xmldoc.xpath('//tc:geo/tc:gpoint/@lat', namespaces={'tc': 'http://www.dspin.de/data/textcorpus'})
longitudes = xmldoc.xpath('//tc:geo/tc:gpoint/@lon', namespaces={'tc': 'http://www.dspin.de/data/textcorpus'})


# Import the basemap package
from mpl_toolkits.basemap import Basemap

# Create a map on which to draw.  We're using a mercator projection, and showing the whole world.
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
# Draw coastlines, and the edges of the map.
m.drawcoastlines()
m.drawmapboundary()
# Convert latitude and longitude to x and y coordinates
x, y = m(list(airports["longitude"].astype(float)), list(airports["latitude"].astype(float)))
# Use matplotlib to draw the points onto the map.
m.scatter(x,y,1,marker='o',color='red')
# Show the plot.
plt.show()
