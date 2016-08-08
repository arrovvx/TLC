import thinkINTF as think
import json


#start the websocket server
def handleData(self, x):
	#do AI stuff here for dynamic learning
	print x

think.startServer(handleData)



#if just want to pull mongodb data
#just call getEntry with the signalGroupID use to tag the signals
#syntax: think.getEntry(signalGroupID)
# e.g. think.getEntry(1469759618440)

#***MAKE SURE YOU CHANGE THE MONGODB IP ADDRESS IN thinkINTF.py***

