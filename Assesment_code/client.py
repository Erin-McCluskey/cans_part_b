import socket
import sys
from common import socket_to_screen, keyboard_to_socket, check_file_exists, send_request

def instruction_error():
	print("Your instruction is invalid use the following template with either(put, get or list): python client.py localhost 6789 get test2.txt ")
	exit()

def check_instruction_valid():
	if len(sys.argv) <=3 :
		instruction_error()

	instruction = sys.argv[3]
	valid_instr = ["get", "put", "list"]
	if instruction not in valid_instr:
		instruction_error()

	if instruction != "list":
		filename = sys.argv[4]
		exists = check_file_exists(side="client", filename=filename)

		if instruction == "get" and exists == True:
			print("File already exists and cannot be overwritten.")
			exit()
		elif instruction == "put" and exists == False:
			print("File trying to upload does not exist.")
			exit()
		return instruction, filename
	return instruction, None

def get(instr, filename):
	pass

def put(instr, filename):
	pass

def list(instr, filename):
	pass

def main():
	# Create the socket with which we will connect to the server
	cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# The server's address is a tuple, comprising the server's IP address or hostname, and port number
	srv_addr = (sys.argv[1], int(sys.argv[2])) # sys.argv[x] is the x'th argument on the command line

	# Convert to string, to be used shortly
	srv_addr_str = str(srv_addr)

	"""
	Enclose the connect() call in a try-except block to catch
	exceptions related to invalid/missing command-line arguments, 
	port number out of range, etc. Ideally, these errors should 
	have been handled separately.
	"""
	try:
		print("Connecting to " + srv_addr_str + "... ")

		"""
		Connect our socket to the server. This will actually bind our socket to
		a port on our side; the port number will most probably be in the
		ephemeral port number range and may or may not be chosen at random
		(depends on the OS). The connect() call will initiate TCP's 3-way
		handshake procedure. On successful return, said procedure will have
		finished successfully, and a TCP connection to the server will have been
		established.
		"""

		cli_sock.connect(srv_addr)

	except Exception as e:
		# Print the exception message
		print(e)
		# Exit with a non-zero value, to indicate an error condition
		exit(1)

	"""
	Surround the following code in a try-except block to account for
	socket errors as well as errors related to user input. Ideally
	these error conditions should be handled separately.
	"""
	try:
		# Loop until either the server closes the connection or the user requests termination
		while True:
			# checks the input instruction valid
			instr, filename = check_instruction_valid()

			#calls the function related to the instruction
			functions = {"get": get, "put": put, "list":list}
			functions[instr](instr, filename)

			bytes_sent = send_request(cli_sock)
			break
			"""
			# First, read data from keyboard and send to server
			bytes_sent = keyboard_to_socket(cli_sock)
			if bytes_sent == 0:
				print("User-requested exit.")
				break

			# Then, read data from server and print on screen
			bytes_read = socket_to_screen(cli_sock, srv_addr_str)
			if bytes_read == 0:
				print("Server closed connection.")
				break
			"""

	finally:
		"""
		If an error occurs or the server closes the connection, call close() on the
		connected socket to release the resources allocated to it by the OS.
		"""
		cli_sock.close()

	# Exit with a zero value, to indicate success
	exit(0)

main()