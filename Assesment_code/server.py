import socket
import sys
import os
from common import *

# Create the socket on which the server will receive new connections
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def check_args(cli_sock, errors, cli_addr, request):
	instruction = request[0]
	valid_instructions = ["get", "put", "list"]

	if (len(request) < 1) or  instruction not in valid_instructions:
		errors.append("Your request is invalid use the following template with either(put, get or list): python client.py localhost 6789 get test2.txt")
		generate_report(cli_sock, str(cli_addr[0]), str(cli_addr[1]), "Invalid", "Failed", str(errors ))
	return instruction

def check_valid_files(instruction, cli_sock, errors, cli_addr, filename):
	exists, file_path = check_file_exists(side="server", filename=filename)

	if exists == True:
		filename = file_path
		if os.path.getsize(filename) <= 0:
			errors.append("This file is empty")

		elif instruction == "put":
			errors.append("File already exists and cannot be overwritten.")

	elif instruction == "get" and exists == False:
		errors.append("File trying to download does not exist.")

	if len(errors) != 0:
		generate_report(cli_sock, str(cli_addr[0]), str(cli_addr[1]), instruction, "Failed", str(errors ), filename=filename)
	filename = file_path
	return instruction, filename

def check_instruction_valid(request, cli_addr):
	errors = []
	request = request.split(" ")
	instruction = check_args(cli_sock, errors, cli_addr, request)

	if instruction == "list":
		return instruction, None

	return check_valid_files(instruction, cli_sock, errors, cli_addr, filename= request[1])

def put(cli_sock, filename, cli_addr):
	try:
		data = recv_one_message(cli_sock)
		recv_file(cli_sock, filename, data)
		generate_report(cli_sock, str(cli_addr[0]), str(cli_addr[1]), "put", "Success", "None", filename=filename)
	except Exception as e:
		generate_report(cli_sock, str(cli_addr[0]), str(cli_addr[1]), "put", "Failed", str(e), filename=filename)

def get(cli_sock, filename, cli_addr):
	try:
		send_file(cli_sock, filename)
	except Exception as e:
		generate_report(cli_sock, str(cli_addr[0]), str(cli_addr[1]), "get", "Failed", str(e), filename=filename)

def list(cli_sock, filename, cli_addr):
	try:
	    send_listing(cli_sock)
	except Exception as e:
		generate_report(cli_sock, str(cli_addr[0]), str(cli_addr[1]), "list", "Failed", str(e), filename=filename)



"""
 Enclose the following two lines in a try-except block to catch
 exceptions related to already bound ports, invalid/missing
 command-line arguments, port number out of range, etc. Ideally,
 these errors should have been handled separately.
"""
try:
	"""
	 Register the socket with the OS kernel so that messages sent
	 to the user-defined port number are delivered to this program.
	 Using "0.0.0.0" as the IP address so as to bind to all available
	 network interfaces. Alternatively, could have used "127.0.0.1"
	 to bind only to the local (loopback) interface, or any other IP
	 address on an interface of the computer where this program is
	 running (use "ipconfig /all" to list all interfaces and their IP
	 addresses).
	"""
	srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) # sys.argv[1] is the 1st argument on the command line

	"""
	 Create a queue where new connection requests will be added by
	 the OS kernel. This number should be small enough to not waste
	 resources at the OS level, but also large enough so that the
	 connections queue doesn't fill up. For this latter, one should
	 ideally have an idea of how long it takes to serve a request
	 and how frequently clients initiate new connections to the
	 server.
	"""
	srv_sock.listen(5)
except Exception as e:
	# Print the exception message
	print(e)
	# Exit with a non-zero value, to indicate an error condition
	exit(1)

# Loop forever (or at least for as long as no fatal errors occur)
while True:
	"""
	 Surround the following code in a try-except block to account for
	 socket errors as well as errors related to user input. Ideally
	 these error conditions should be handled separately.
	"""
	try:
		print("Waiting for new client... ")

		"""
		 Dequeue a connection request from the queue created by listen() earlier.
		 If no such request is in the queue yet, this will block until one comes
		 in. Returns a new socket to use to communicate with the connected client
		 plus the client-side socket's address (IP and port number).
		"""
		cli_sock, cli_addr = srv_sock.accept()
		cli_addr_str = str(cli_addr) # Translate the client address to a string (to be used shortly)

		print(f"Client IP address: {cli_addr[0]}, Client Port number: {cli_addr[1]}, Server up and running.")

		# Loop until either the client closes the connection or the user requests termination
		#while True:
		# First, read data from client and print on screen
		request = []
		request = recv_request(cli_sock, cli_addr, request)

		# if request == None or len(request) == 0:
		# 	print("Client closed connection.")
		# 	break

		instr, filename = check_instruction_valid(request, cli_addr)
		#parse the users request
		functions = {"get": get, "put": put, "list":list}
		functions[instr](cli_sock, filename, cli_addr)

	finally:
		"""
		 If an error occurs or the client closes the connection, call close() on the
		 connected socket to release the resources allocated to it by the OS.
		"""
		cli_sock.close()

# Close the server socket as well to release its resources back to the OS
srv_sock.close()

# Exit with a zero value, to indicate success
exit(0)
