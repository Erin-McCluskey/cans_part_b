Erin McCluskey - 2842838m					Callum Duncan Smith - 2905031s

 

Introduction: 

We have used the knowledge we have acquired in this second part of the course to build a networked application. Our application consists of a Server Python script – that receives and deals with client requests for files stored in a local directory - and a Client Python Script - that allows users to upload or download files from the server, as well as list the files currently stored on the server. As part of the application, we also use a common python file to store functions which could be used by both the server and the client to minimise redundant code. 

What kind of messages are transferred between the client and server: 

 

Handshake Messages: 

First the Client sends a hello to the server which Initiates the connection to the server. The Server will then reply with its own Hello which acknowledges the Client's connection request and provides necessary session information. 

 

File Transfer Messages: 

Get File:  

The Get request is sent by the client to request a specific file from the server. The server will then respond with either the data of the requested file then a success message indicating a successful completion of the file transfer or, a file not found error if the requested file is not available. 

Put File: 

The Put request is sent by the client to Upload a specific file to the server. The server will then respond with a success message if it managed to upload the file or, an error message if something did not go as planned. 

List File: 

The List request is sent by the client to the server. The server will then respond with a list of the files that are available to download. 

 

Error Handling Messages: 

Sent by either the client or the server to show to the user if any errors occur during the file transfer process. 

How did we ensure exact number of bytes are sent/received? 

When sending the initial requests from the client to the server we do not account for the number of bytes being sent and received as there is enough idle time on the CPU to run the sending of the request on the client side before the server tries to read this data. This is not true however for the sending larger data transfers such as is necessary for the data transfer of the contents of the file. 

For transferring the content to be stored within a file we used a simple protocol to ensure that the correct number of bytes are sent and received. This involves creating a byte stream which sends the message along with the information required to know where messages begin and end. For this to be achieved we first send the length of the data about to be transferred so that the receiver knows exactly how much of the data is expected to be unpacked and then sends the packed data. 

 

Error Handling: 

We created a generate report function that was called upon nearly every time there was a chance an error could throw. This would display to the user if a transfer was successful and the errors, if any, that had arisen. We covered errors such as invalid input, the filename not being provided, the filename being too long, the file being empty and the file already existing. 