
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
from pymongo import MongoClient

client = MongoClient('mongodb://dockerhost:27017/')
db = client.EMG

signalGroupID = 0;
signalCursor = 0;


def startServer(msgHandler): #
	class WSHandler(tornado.websocket.WebSocketHandler):
		def check_origin(self, origin):
			return True

		def open(self):
			print 'connection opened...'
			self.write_message("The server says: 'Hello'. Connection was accepted.")

		def on_message(self, message):
			msgHandler(self, message)
			#self.write_message("2")#The server says: " + message + " back at you
			print 'received:', message

		def on_close(self):
			print 'connection closed...'
			
	application = tornado.web.Application([
	  (r'/', WSHandler),
	])
	application.listen(8890)
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
	






