import traci
import traci.constants as tc
import pandas as pd

##################################
# Experimental preparation
##################################
folder = "E:/sumo-map/2021-04-29-14-04-53/"

sumoBinary = "sumo"
sumoCmd = [sumoBinary, "-c", folder + "osm.sumocfg"]

try:
    traci.close() # Ensure that the last trace connection closes normally
except Exception:
    pass
traci.start(sumoCmd)  # Execute sumo-gui on the command line to start the simulation

# Get detectors list
detectors = []
detect_id = traci.inductionloop.getIDList() 
for i in detect_id:
		if i[0] == 'e':
			detectors.append(i)

outlist = pd.DataFrame(data = detectors)
outlist.to_csv('detectors_0429.csv')
# print(e1det_id)

traci.close()