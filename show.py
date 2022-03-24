##################################
# Experimental preparation
##################################
import pandas as pd
folder = "E:/sumo-map/2021-04-29-14-04-53/"

# Load the sensor list
corpus = pd.read_csv('detectors_list.csv')
corpus = corpus.values.tolist()
detectors = []
for val in corpus:
    detectors.append(val[1])

##################################
# Statistical sensor data
##################################
from xml.dom import minidom
DOMTree = minidom.parse(folder + 'e1output.xml')
collection = DOMTree.documentElement

records = collection.getElementsByTagName('interval')
flowRcds = {}
occRcds = {}
speedRcds = {}

def insertRcd(aDict, id, str_val):
    if id not in aDict:
        aDict[id] = []
    val = float(str_val)
    aDict[id].append(val)

for record in records:
    id = record.getAttribute('id')
    if id in detectors:
        flow = record.getAttribute('flow')
        occupancy = record.getAttribute('occupancy')
        speed = record.getAttribute('speed')
        insertRcd(flowRcds, id, flow)
        insertRcd(occRcds, id, occupancy)
        insertRcd(speedRcds, id, speed)

##################################
# Occupancy
##################################
import matplotlib.pyplot as plt

for i in range(len(detectors)):
    id = detectors[i]
    plt.title('Occupancy of %d detectors' % len(detectors))
    plt.plot(occRcds[id])
    plt.ylim((0, 120))
#     plt.show()
plt.legend()
plt.show()


##################################
# Flow
##################################
import matplotlib.pyplot as plt

for i in range(len(detectors)):
    id = detectors[i]
    plt.title('Flow of %d detectors' % len(detectors))
    plt.plot(flowRcds[id])
    plt.ylim((0, 1750))
    #     plt.show()
plt.legend()
plt.show()

##################################
# Speed
##################################
import matplotlib.pyplot as plt

for i in range(len(detectors)):
    id = detectors[i]
    plt.title('Speed of %d detectors' % len(detectors))
    plt.plot(speedRcds[id])
    plt.ylim((0, 20))
    #     plt.show()
plt.legend()
plt.show()