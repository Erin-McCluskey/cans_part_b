import sys
import socket
import struct
import time
import os
from os import listdir
from os.path import isfile, join

def recv_request(socket, cli_addr, request):
    request = ""
    while len(request) == 0:
        data = bytearray(1)
        request = ""

        data = socket.recv(4096)
        request += data.decode()

        if request == "invalid":
            generate_report(socket, str(cli_addr[0]), str(cli_addr[1]), "Invalid", "Failed", "[Request was formatted incorrectly]")
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
    # Generates and sends the directory listing from the server to the client.
    files = os.listdir(os.path.join(os.getcwd(), "server_data"))
    print(files)

    bytes_sent = socket.sendall("\n".join(files).encode())
    return bytes_sent

def recv_listing(socket):
	#Receives the listing from the server via the provided socket and prints it onscreen.
	data = bytearray(1)
	bytes_read = 0

	data = socket.recv(4096)
	bytes_read += len(data)

	files_in_server = data.decode().split()

	return files_in_server


def generate_report(socket, IP, port_number, request_type, status, errors, filename = "None"):
    socket.sendall(str.encode("invalid"))
    print("IP: " + IP + ", port number: "+ port_number + ", request type: " + request_type + ", Filename: "+ filename +", Status: " + status + ", Errors encountered: " + errors)
    socket.close()
    exit(1)

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
