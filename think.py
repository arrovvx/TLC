import thinkINTF as think
import json

a = []
def handleData(self, x):
	#print x
	jsonData = json.loads(x)
	
	if len(a) > 20:
		a.pop(0)
	
	a.append(jsonData['input'][0])
	sum = 0;
	average = 0;
	for value in a:
		sum = sum + value
	
	average = sum / len(a)
	
	
	print "average " + str(average)
	if average < 700:
		self.write_message("1")
	else:
		self.write_message("2")

think.startServer(handleData)
think.getEntry(1469759618440)
think.getEntry(1469759618440)
think.getEntry(1469759618440)
think.getEntry(1469759618440)


#think.getEntry()

