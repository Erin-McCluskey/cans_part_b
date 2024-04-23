# Assesment info

### File structure
<project_folder>/
    server.py
    client.py
    common_utilitities.py

    server_data/
    ... data files on the server

    client_data/
    ... data files on the client

### Running the chats
Use the code provided in the tutorial model
 - run the server by opening a powershell terminal and entering python server.py <port number> e.g python server.py 200

    should output waiting for client

 - run the client by opeining a diffrent powershell terminal and entering python myclient.py localhost <port number> <message> e.g python myclient.py localhost 2000 "this is my message"

    should output Connecting to ('localhost', <port number>)...
    Connected. Now chatting...

### Scripts goals
### common
Add any functions to be used by both server and client to here.

Function examples:
- send_file(socket,filename):
    Opens the file with the given filename and sends its data over the net-work through the provided socket

- recv_file(socket, filename):
    Creates the file with the given filename and stores into it data received from the provided socket

- send_listing(socket):
    Generates and sends the directory listing from the server to the client via the provided socket

- recv_listing(socket)
    Receives the listing from the server via the provided socket and prints it onscreen.

#### Server
- set hostname as “0.0.0.0” or an empty string
- Set up connection and print in one line ip address + port number + text"server up and running"
- for each connection (returned by socket.accept()) do the following:
    - parse the request
    - execute each request
    - close the connection

##### Request types
- Upload a file
    Client request - request type, filename, data to put in file
    - Deny if file exists to avoid overwriting
    - Create file in exclusive creation binary mode
    - Put the data from the socket to the file
    - Print report

- Download a file
    Client request - request type, filename
    - Check file to be downloaded exists
    - Open the file in binary mode
    - Write data to the client through the socket
    - Print report

- List the 1st level directory contents
    Client request - request type
    - Gets a list of top level directories (using os.listdir())
    - Write directories back to client over socket
    - Print report

- Report content
    - IP address
    - port number of client
    - request time
    - filename (if applicable)
    - status (success/failure)
    - if failure should also have error message with error type
    - Any other error encountered in execution

#### Client goals
Arguments are passed in from command line
Arguments passed in = address of server(hostname or ip), servers port number, request type(put, get, list)

To do this run the following type of command in powershell. (This request will execute all request types retrospectivly you can pass in any variation of put get and list)
    python client.py <hostname> <port> <put filename|get filename|list>
    e.g.
    python client.py localhost 6789 get test2.txt

#### functionality
 - parse the command line arguments
 - create a client socket
 - connect to server defined in command line
 - format and send appropriate response
 - Send request to client
 - end connection

 #### request types
 - upload (put)
    - open file in binary mode
    - read in data in file
    - send to server
    - close connection

 - download (get)
    - open file in binary mode
    - read in data sent by server
    - store in file
    - close connection

 - listing (list)
    - send request message
    - recieve the listing from server
    - print (one line per file name)
    - close connection

- Report content
    - IP address
    - port number of client
    - request time
    - filename (if applicable)
    - status (success/failure)
    - if failure should also have error message with error type
    - Any other error encountered in execution

### Marking scheme
-  70 marks for the implementation
    - 15 marks for the implementation of the “list” request type
    - 25 marks for each of “put”/“get” request types
-  30 marks for the report

#### Implementation breakdown:
All request types:
-  9 marks for handling the intricacies of TCP communication – i.e., that data is streamed from the source to the destination and hence data sent via a single send()/sendall() call may be fragmented and received across several sequential recv() calls, or data sent via multiple send()/sendall() calls may be collated and returned through a single recv() call.
- 3 marks for handling of connection failures mid-way through the protocol.
- 2 marks for appropriate logging/reporting.
- 1 mark for parsing of command line arguments. 

Only for “put”/“get” requests:
-  5 marks for correct handling/transferring of binary data (binary transfer, byte ordering, etc.).
-  5 marks for support for stability/security features such as very large files, 0-sized files, no overwriting of existing files, very long filenames, etc.
- 5 marks for appropriate structure of your code (functions, minimal repetition of code, informative but not excessive comments, etc.).

#### Report breakdown
- 20 marks for the quality of the design of the application-level protocol.
- 10 marks for the discussion of the reasoning/design decisions.

### What to submit
For this assessed exercise, you can work on your own, or groups of two. Submit azip file CANS2024-AE2-your-student-id.zip

#### Zip should include
- python source code files
- report as a README

#### The report include
- a heading stating the full name(s) and matriculation number(s) of the team member(s)
- include a detailed description of the application-level protocol you designed (exact format of the exchanged messages, their fields and
semantics, the order in which these messages are expected to be exchanged,etc.)
- a discussion of the reasoning behind the design of your protocol and the associated design decisions. 

Only ONE (1) submission should be done per team. Any one of the team members can upload the submission via their Moodle account. Please make sure your submission clearly states the names of both students if you are submitting as a team of two