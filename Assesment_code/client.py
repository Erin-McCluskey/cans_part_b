import socket
import sys
import os
from common import check_file_exists, send_request, send_file, generate_report, recv_file, recv_one_message

def check_args(cli_sock, errors, srv_addr):
	if len(sys.argv) <=3 :
		errors.append("Your instruction is invalid use the following template with either(put, get or list): python client.py localhost 6789 get test2.txt")
		generate_report(cli_sock, str(srv_addr[0]), str(srv_addr[1]), "Invalid", "Failed", str(errors ))

def check_valid_instruction(instruction, cli_sock, errors, srv_addr):
	valid_instr = ["get", "put", "list"]
	if instruction not in valid_instr:
		errors.append("Your instruction is invalid use the following template with either(put, get or list): python client.py localhost 6789 get test2.txt")
		generate_report(cli_sock, str(srv_addr[0]), str(srv_addr[1]), "Invalid", "Failed", str(errors ))

def check_valid_files(instruction, cli_sock, errors, srv_addr):
	if len(sys.argv)<=4:
		errors.append("Filename not provided")
		generate_report(cli_sock, str(srv_addr[0]), str(srv_addr[1]), instruction, "Failed", str(errors ))

	filename = sys.argv[4]
	if len(filename) > 50:
		errors.append("Filename too long")

	exists, file_path = check_file_exists(side="client", filename=filename)

	if exists == True:
		if os.path.getsize(filename) <= 0:
			errors.append("This file is empty")

		elif instruction == "get":
			errors.append("File already exists and cannot be overwritten.")

	elif instruction == "put" and exists == False:
		errors.append("File trying to upload does not exist.")

	if len(errors) != 0:
		generate_report(cli_sock, str(srv_addr[0]), str(srv_addr[1]), instruction, "Failed", str(errors ), filename=filename)
	filename = file_path
	return instruction, filename

def check_instruction_valid(cli_sock, srv_addr):
	errors = []
	check_args(cli_sock, errors, srv_addr)

	instruction = sys.argv[3]
	check_valid_instruction(instruction, cli_sock, errors, srv_addr)

	if instruction == "list":
		return instruction, None

	return check_valid_files(instruction, cli_sock, errors, srv_addr)

def get(filename, cli_sock, srv_addr):
	try:
		send_request(cli_sock)
		data = recv_one_message(cli_sock)
		recv_file(cli_sock, filename, data)
		generate_report(cli_sock, str(srv_addr[0]), str(srv_addr[1]), "get", "Success", "None", filename=filename)
	except Exception as e:
		generate_report(cli_sock, str(srv_addr[0]), str(srv_addr[1]), "get", "Failed", str(e), filename=filename)

def put(filename, cli_sock, srv_addr):
	try:
		send_request(cli_sock)
		send_file(cli_sock, filename)
	except Exception as e:
		generate_report(cli_sock, str(srv_addr[0]), str(srv_addr[1]), "put", "Failed", str(e), filename=filename)

def list(filename, cli_sock):
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
		# checks the input instruction valid
		instr, filename = check_instruction_valid(cli_sock, srv_addr)

		#calls the function related to the instruction
		functions = {"get": get, "put": put, "list":list}
		functions[instr](filename, cli_sock, srv_addr)

	finally:
		"""
		If an error occurs or the server closes the connection, call close() on the
		connected socket to release the resources allocated to it by the OS.
		"""
		cli_sock.close()

	# Exit with a zero value, to indicate success
	exit(0)

main()