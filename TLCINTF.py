
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.99.100:27017/')#dockerhost
db = client.EMG

signalGroupID = 0;
signalCursor = 0;


#this is just for dev
is_closing = False
def try_exit(): 
    global is_closing
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('exit success')

def startServer(msgHandler): #
	class WSHandler(tornado.websocket.WebSocketHandler):
		def check_origin(self, origin):
			return True

		def open(self):
			print('connection opened...')
			#self.write_message("The server says: 'Hello'. Connection was accepted.")

		def on_message(self, message):
			response = msgHandler(self, message)
			self.write_message('{"output": '+ str(response) + '}')#The server says: " + message + " back at you
			print('received:', message)

		def on_close(self):
			print('connection closed...')
			
	application = tornado.web.Application([
	  (r'/', WSHandler),
	])
	application.listen(8890)
	tornado.ioloop.PeriodicCallback(try_exit, 1000).start() 
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
	






