import traci
import traci.constants as tc
import pandas as pd

##################################
# configuration parameters
##################################
# Simulation file path
folder = "E:/sumo-map/2021-04-29-14-04-53/"

# reading detectors list
corpus = pd.read_csv('detectors_list.csv')
corpus = corpus.values.tolist()
detectors = []
for val in corpus:
    detectors.append(val[1])

# collect detector data
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
# remove useless data
##################################
thre = 40
for id in detectors:
	tag = 0 
	for val in occRcds[id]:
		if val > 40:
			tag = 1
			break

	if tag == 0:
		detectors.remove(id)


##################################
# Data smoothing
##################################
for id in detectors:
	pre_data = occRcds[id]
	aft_data = []
	# smoothing
	for i in range(len(pre_data)):
		if i == 0:
			aft_data.append(pre_data[i])
		else:
			aft_data.append(0.75 * pre_data[i] + 0.25 * aft_data[i-1])

	occRcds[id] = aft_data

##################################
# DSA
##################################
for id in detectors:
	pre_data = occRcds[id]
	aft_data = []
	# DSA变换
	for i in range(len(pre_data)):
		if i == 0:
			aft_data.append(pre_data[i+1] - pre_data[i])
		elif i == len(pre_data) - 1:
			aft_data.append(pre_data[i] - pre_data[i-1])
		else:
			aft_data.append((pre_data[i+1]-pre_data[i-1])/2)

	occRcds[id] = aft_data


##################################
# FAD
##################################
epsi = 1.1
for id in detectors:
	pre_data = occRcds[id]
	aft_data = []
	for i in range(len(pre_data)):
		aft_data.append(int(pre_data[i] / epsi))
		# print(aft_data[i])

	occRcds[id] = aft_data

##################################
# Z-score
##################################
epsi = 3.5

def get_median(data):
    tmp_data = []
    for i in range(len(data)):
        tmp_data.append(data[i])
    tmp_data.sort()
    half = len(tmp_data) // 2
    return (tmp_data[half] + tmp_data[~half]) / 2

for id in detectors:
    pre_data = occRcds[id]
    R = get_median(pre_data)
    MAD_ls = []
    for i in range(len(pre_data)):
        MAD_ls.append(abs(pre_data[i]-R))
    MAD = get_median(MAD_ls)
    aft_data = [] 
    for i in range(len(pre_data)):
        if MAD == 0:
            aft_data.append(0)
            continue
        Mi = (0.6745 * (pre_data[i]-R)) / MAD
        if Mi >= epsi:
            aft_data.append(1)
        else:
            aft_data.append(0)

    occRcds[id] = aft_data

##################################
# OBADA-MV
##################################
block_size = 3
def get_majority(data):
    sum = 0
    for val in data:
        sum += val
    if sum >= 2:
        return 1
    else:
        return 0

for id in detectors:
    pre_data = occRcds[id]
    for i in range(block_size, len(pre_data) - block_size):
        if get_majority(pre_data[i-block_size:i-1]) or get_majority(pre_data[i+1:i+block_size]):
            pre_data[i] = 1
        else:
            pre_data[i] = 0


##################################
# Show results
##################################
import matplotlib.pyplot as plt

for i in range(len(detectors)):
    id = detectors[i]
    plt.title('Occupancy of %d detectors' % len(detectors))
    plt.plot(occRcds[id])
    plt.ylim((0, 2))
#     plt.show()
plt.legend()
plt.show()