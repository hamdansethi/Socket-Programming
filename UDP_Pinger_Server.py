import sys
from socket import *

port = 8888

if port < 0 or port > 65535:
    print("Error: Port must be in the range 0-65535.")
    sys.exit(1)

serversocket = socket(AF_INET, SOCK_DGRAM)
serversocket.bind(('', port))
print(f"UDP server up and listening on port {port}...")

while True:
    message, client_address = serversocket.recvfrom(1024)
    print(f"Received message: {message.decode()} from {client_address}")

    serversocket.sendto("Hello".encode(), client_address)
    print(f"Sent response to {client_address}")
