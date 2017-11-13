import socket

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('localhost', 8080))
client_socket = socket.socket()
host = socket.gethostname()
port = 8080
client_socket.bind((host, port))

data = client_socket.recv(256)
while data[-1] != b'0':
    data += client_socet.recv(256)

print("RECEIVED:" , data)

# parrot back
client_socket.send(data)
# client_socket.close()
