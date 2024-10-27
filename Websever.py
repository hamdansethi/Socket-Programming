import socket
import sys

serverPort = 8080

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))

serverSocket.listen(1)
print(f"The server is ready to receive on port {serverPort}...")

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Received a connection from: {addr}")

    try:
        request = connectionSocket.recv(1024).decode()
        print(f"Request:\n{request}")

        request_line = request.splitlines()[0]
        print(request_line)
        filename = request_line.split()[1]

        if filename.startswith('/'):
            filename = filename[1:]

        with open(filename, 'r') as f:
            outputdata = f.read()

            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += "Content-Length: {}\r\n".format(len(outputdata))
            response_header += "\r\n"

            connectionSocket.send(response_header.encode())
            connectionSocket.send(outputdata.encode())

    except IOError:
        response_header = "HTTP/1.1 404 Not Found\r\n"
        response_header += "Content-Type: text/html\r\n"
        response_header += "\r\n"
        response_body = "<html><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(response_header.encode())
        connectionSocket.send(response_body.encode())

    finally:
        connectionSocket.close()
