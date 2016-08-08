import TLCINTF as TLC
import json


#start the websocket server
def handleData(self, x):
	#do AI stuff here for dynamic learning
	print x

TLC.startServer(handleData)



#if just want to pull mongodb data
#just call getEntry with the signalGroupID use to tag the signals
#syntax: TLC.getEntry(signalGroupID)
# e.g. TLC.getEntry(1469759618440)

#***MAKE SURE YOU CHANGE THE MONGODB IP ADDRESS IN TLCINTF.py***

