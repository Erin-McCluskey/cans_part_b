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

### What to submit