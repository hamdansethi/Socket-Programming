import sys, time
from socket import *

argv = sys.argv                      
host = '192.168.0.108'
port = 8888
timeout = 1 

clientsocket = socket(AF_INET, SOCK_DGRAM)
clientsocket.settimeout(timeout)

port = int(port)  
ptime = 0  


while ptime < 10: 
	ptime += 1
	data = "Ping " + str(ptime) + " " + time.asctime()
    
	try:
		RTTb = time.time()

		clientsocket.sendto(data.encode(),(host, port))
		message, address = clientsocket.recvfrom(1024)  

		RTTa = time.time()

		print("Reply from " + address[0] + ": " + message.decode())       
		print("RTT: " + str(RTTa - RTTb))
	except:
		print ("Request timed out.")
		continue


clientsocket.close()
 




