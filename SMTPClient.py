import socket
import ssl
import base64

email = "mxnkxydlxfffy@gmail.com"
password = "trtt djzt rkae vvlr"
msg = 'I love computer networks!'
endmsg = '\r\n.\r\n'
mailserver = 'smtp.gmail.com'
port = 587

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver, port))
recv = clientSocket.recv(1024).decode()
print(recv)

heloCommand = 'HELO gmail.com\r\n'
clientSocket.send(heloCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.send(b'STARTTLS\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

clientSocket.send(heloCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.send(b'AUTH LOGIN\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.send(base64.b64encode(email.encode()) + b'\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

if recv[:3] != '235':
    print('Authentication failed.')
    clientSocket.close()
    exit()

clientSocket.send(f'MAIL FROM: <{email}>\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

recipient_email = 'hamdansethi003@gmail.com'
clientSocket.send(f'RCPT TO: <{recipient_email}>\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.send(b'DATA\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.send(b'SUBJECT: Test Email\r\n\r\n')
clientSocket.send(msg.encode() + endmsg.encode())

recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.send(b'QUIT\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.close()
