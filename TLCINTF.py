import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

import json
import numpy as np
import pywt as pywt
import threading

from pymongo import MongoClient

with open('settings.json') as settings_file:    
    settings = json.load(settings_file)

#wavelet transform constants
shiftSpeed = settings['shiftSpeed']
windowSize = settings['windowSize']

#wavelet transform variables
shiftEnd = windowSize - shiftSpeed
fillNum = windowSize // shiftSpeed
transformWindow = [0] * windowSize
targetWindow = [0] * windowSize
runNum = 0
bufferData = [0] * shiftSpeed
bufferTarget = [0] * shiftSpeed
curser = 0

#mongoDB access variables
client = MongoClient('mongodb://'+ str(settings['databaseIP']) +':'+ str(settings['databasePort']) +'/')
db = client.EMG#[settings['databaseName']]
signalGroupID = 0
signalCursor = 0

#start the websocket server
def startServer(msgHandler):
	
	class WSHandler(tornado.websocket.WebSocketHandler):
		
		def check_origin(self, origin):
			return True

		def open(self):
			print('connection opened...')
			reInitVal()
			#self.write_message("The server says: 'Hello'. Connection was accepted.")

		def on_message(self, message):
			handleMsg(self, message, msgHandler)

		def on_close(self):
			print('connection closed...')
			
	application = tornado.web.Application([
	  (r'/', WSHandler),
	])
	application.listen(settings['TLCWebsocketPort']) 
	tornado.ioloop.PeriodicCallback(try_exit, 1000).start() #for dev exit in terminal
	tornado.ioloop.IOLoop.instance().start()


def getEntry(signalGroupID):
	global signalCursor;
	
	result = db.signals.find_one({"signalGroupID":signalGroupID,"timeStamp":{"$gt": signalCursor}})
	if result:
		signalCursor = result["timeStamp"]; #update the cursor with timestamp
		del result["_id"]
		#del result["timeStamp"]
		del result["signalGroupID"]
		
		print(result)
		
		return result
		
	return None
	
def resetCursor():
	signalCursor = 0;
	
def reInitVal():
	global windowSize,shiftSpeed,shiftEnd,bufferData,bufferTarget, fillNum, curser, buffer, transformWindow, targetWindow, runNum
	
	#wavelet transform variables
	shiftEnd = windowSize - shiftSpeed
	fillNum = windowSize // shiftSpeed
	transformWindow = [0] * windowSize
	targetWindow = [0] * windowSize
	runNum = 0
	bufferData = [0] * shiftSpeed
	bufferTarget = [0] * shiftSpeed
	curser = 0
	
	
def handleMsg(self, message, callback):
	global shiftEnd,bufferData,bufferTarget, fillNum, curser, buffer, transformWindow, targetWindow, runNum
	
	parsed_json = json.loads(message)
	bufferData[curser] = parsed_json['input']
	bufferTarget[curser] = parsed_json['output']
	
	curser += 1
	if(curser == shiftSpeed):
		curser = 0
		transformWindow[shiftSpeed:] = transformWindow[:shiftEnd]
		transformWindow[:shiftSpeed] = bufferData[:shiftSpeed]
		
		targetWindow[shiftSpeed:] = targetWindow[:shiftEnd]
		targetWindow[:shiftSpeed] = bufferTarget[:shiftSpeed]
		
		if (runNum > fillNum):
			Data = np.array(transformWindow)
			Target = np.array(targetWindow)
			
			aa, ff = pywt.cwt(Data[:,0], np.arange(1, 129), 'morl')
			DataArr = np.array([aa[:,300:700]])
			
			for i in range(Data.shape[1] - 1):
				aa, ff = pywt.cwt(Data[:,i + 1], np.arange(1, 129), 'morl')
				DataArr = np.vstack([DataArr,[aa[:,300:700]]])
				
			self.write_message('{"output": '+ str(callback(DataArr, Target[300:700])) + '}')
			
			#plt.matshow(aa) 
			#plt.show()
			#thr = threading.Thread(target=runNN, args=(self))#, kwargs={}
			#thr.start() # will run "foo"
		else:
			runNum += 1

#this is just for dev, to close the server in terminal
is_closing = False
def try_exit(): 
    global is_closing
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('exit success')


