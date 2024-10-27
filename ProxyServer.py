from socket import *
import sys
import os

IP_ADDRESS = "192.168.0.108"
PORT = 8888

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((IP_ADDRESS, PORT))
serverSocket.listen(100)

CACHE_DIR = "./cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

while True:
    print("Ready to serve...")

    clientSocket, addr = serverSocket.accept()
    print("Received a connection from: ", addr)

    message = clientSocket.recv(1024).decode('utf-8', errors='ignore')
    print("Received message:\n", message)

    parts = message.split()
    if len(parts) < 3:
        print("Invalid HTTP request")
        clientSocket.send(b"HTTP/1.0 400 Bad Request\r\n\r\n")
        clientSocket.close()
        continue

    method = parts[0]
    url = parts[1]
    hostn = url.split("//")[-1].split("/")[0]
    path = "/".join(url.split("/")[3:])
    print("Host:", hostn)
    print("Path:", path)

    cache_file_path = os.path.join(CACHE_DIR, path.replace("/", "_"))

    if method == "GET":
        try:
            # Try to read from the cache
            with open(cache_file_path, "rb") as f:
                data = f.read()
                clientSocket.send(b"HTTP/1.0 200 OK\r\n")
                clientSocket.send(b"Content-Type: text/html\r\n")
                clientSocket.send(b"\r\n")
                clientSocket.send(data)
                print("Read from cache")
        except IOError:
            print(f"Connecting to {hostn}...")

            c = socket(AF_INET, SOCK_STREAM)
            try:
                c.connect((hostn, 80))
                request = f"GET /{path} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                c.send(request.encode())

                response = bytearray()
                while True:
                    buff = c.recv(4096)
                    if not buff:
                        break
                    response.extend(buff)
            
                clientSocket.send(response)

                with open(cache_file_path, "wb") as tmpFile:
                    tmpFile.write(response)

            except Exception as e:
                print("Illegal Request:", e)
                clientSocket.send(b"HTTP/1.0 404 Not Found\r\n\r\n")
            finally:
                c.close()

    elif method == "POST":
        print("Forwarding POST request to the server...")
        c = socket(AF_INET, SOCK_STREAM)
        try:
            c.connect((hostn, 80))
            c.send(message.encode())
            response = bytearray()
            while True:
                buff = c.recv(4096)
                if not buff:
                    break
                response.extend(buff)
            clientSocket.send(response)
        except Exception as e:
            print("Error forwarding POST request:", e)
            clientSocket.send(b"HTTP/1.0 500 Internal Server Error\r\n\r\n")
        finally:
            c.close()

    else:
        print("Unsupported HTTP method")
        clientSocket.send(b"HTTP/1.0 405 Method Not Allowed\r\n\r\n")

    clientSocket.close()
