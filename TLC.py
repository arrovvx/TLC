import TLCINTF as TLC

import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import math as math
import tensorflow as tf


#this function is called everytime there is a batch of data (400 default, can be changed in settings.json)
#return negetive value for cases where you don't want to return a prediction

def handleData(Data,Target):
	print(Data.shape)
	return 3
	

	
#start the websocket server
TLC.startServer(handleData)



#if just want to pull mongodb data
#just call getEntry with the signalGroupID use to tag the signals
#syntax: TLC.getEntry(signalGroupID)
# e.g. TLC.getEntry(1469759618440)

#***MAKE SURE YOU CHANGE THE MONGODB IP ADDRESS IN TLCINTF.py***

