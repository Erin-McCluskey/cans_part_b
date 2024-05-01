import sys
import socket
import struct
import time
from os import listdir
from os.path import isfile, join

def recv_request(socket):
    data = bytearray(1)
    request = ""

    data = socket.recv(4096)
    request += data.decode()
    return request

def send_request(socket):
    request = " ".join(sys.argv[3:len(sys.argv)]) + " "
    socket.sendall(str.encode(request))

def check_file_exists(side, filename):
    if side == "client":
        path = "client_data"
    else:
        path = "server_data"

    files = [f for f in listdir(path) if isfile(join(path, f))]
    if filename in files:
        return True, path+"/"+filename
    else:
        return False, path+"/"+filename

def send_file(socket,filename):
    #Opens the file with the given filename and sends its data over the net-work through the provided socket
    with open(filename, "rb") as file:
        content = file.read()
    time.sleep(5)
    #print(content)
    send_one_message(socket, content)

def recv_file(socket, filename, data):
    #Creates the file with the given filename and stores into it data received from the provided socket
    open(filename, "x")
    data = data.replace("b", "")
    data = data.replace("'", "")
    data = str.encode(data)
    with open(filename, "wb") as file:
        file.write(data)

def send_listing(socket):
    #Generates and sends the directory listing from the server to the client via the provided socket
    pass
def recv_listing(socket):
    #Receives the listing from the server via the provided socket and prints it onscreen.
    pass

def generate_report(socket, sock_addr):
    pass

def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    data = recvall(sock, length)
    return data.decode()

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf