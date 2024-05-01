import sys
import socket
from os import listdir
from os.path import isfile, join

def socket_to_screen(socket, sock_addr):
	"""Reads data from a passed socket and prints it on screen.

	Returns either when a newline character is found in the stream or the connection is closed.
		The return value is the total number of bytes received through the socket.
	The second argument is prepended to the printed data to indicate the sender.
	"""
	print(sock_addr + ": ", end="", flush=True) # Use end="" to avoid adding a newline after the communicating partner's info, flush=True to force-print the info

	data = bytearray(1)
	request = ""

	"""
	 Loop for as long as data is received (0-length data means the connection was closed by
	 the client), and newline is not in the data (newline means the complete input from the
	 other side was processed, as the assumption is that the client will send one line at
	 a time).
	"""
	while len(data) > 0 and "\n" not in data.decode():
		"""
		 Read up to 4096 bytes at a time; remember, TCP will return as much as there is
		 available to be delivered to the application, up to the user-defined maximum,
		 so it could as well be only a handful of bytes. This is the reason why we do
		 this in a loop; there is no guarantee that the line sent by the other side
		 will be delivered in one recv() call.
		"""
		data = socket.recv(4096)
		request += data.decode()
		#print(request, end="") # Use end="" to avoid adding a newline per print() call
		#bytes_read += len(data)
	return request

def keyboard_to_socket(socket):
	"""Reads data from keyboard and sends it to the passed socket.

	Returns number of bytes sent, or 0 to indicate the user entered "EXIT"
	"""
	print("You: ", end="", flush=True) # Use end="" to avoid adding a newline after the prompt, flush=True to force-print the prompt

	# Read a full line from the keyboard. The returned string will include the terminating newline character.
	user_input = sys.stdin.readline()
	if user_input == "EXIT\n": # The user requested that the communication is terminated.
		return 0

	# Send the whole line through the socket; remember, TCP provides no guarantee that it will be delivered in one go.
	bytes_sent = socket.sendall(str.encode(user_input))
	return bytes_sent

def send_request(socket):
	request = " ".join(sys.argv[3:len(sys.argv)])

	# Send the whole line through the socket; remember, TCP provides no guarantee that it will be delivered in one go.
	bytes_sent = socket.sendall(str.encode(request))
	return bytes_sent

def check_file_exists(side, filename):
	if side == "client":
		path = "client_data"
	else:
		path = "server_data"

	files = [f for f in listdir(path) if isfile(join(path, f))]
	if filename in files:
		return True
	else:
		return False

def send_file(socket,filename):
	#Opens the file with the given filename and sends its data over the net-work through the provided socket
	with open(filename, "rb") as file:
		content = file.read()
	bytes_sent = socket.sendall(str.encode(content))
	return bytes_sent

def recv_file(socket, filename):
	#Creates the file with the given filename and stores into it data received from the provided socket
	data = bytearray(1)
	bytes_read = 0
	open(filename, "X")

	while len(data) > 0 and "\n" not in data.decode():
		data = socket.recv(4096)
		bytes_read += len(data)

	with open(filename, "wb") as file:
		bytes_read = file.read()
	return bytes_read

def send_listing(socket, files_in_server):
	#Generates and sends the directory listing from the server to the client via the provided socket
	bytes_sent = socket.sendall(str.encode(files_in_server))
	if bytes_sent == 0:
		print("User-requested exit.")



def recv_listing(socket):
	#Receives the listing from the server via the provided socket and prints it onscreen.
	pass