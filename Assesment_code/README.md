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
    - 