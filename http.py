# Implements a simple HTTP Server
import socket
# Handle the HTTP request.

def handle_request(request):

 # Parse HTTP headers
 headers = request.split('\n')
 fields = headers[0].split()
 request_type = fields[0]
 filename = fields[1]

 print ('Type: %s and Filename: %s' % (request_type, filename))
 # Parse the request type
 if request_type == 'GET':

     
     try:

         if filename == '/':
             filename = '/index.html'
         print ('Filename: ' + filename)
         fin = open('/python' + filename)
         print(fin)
         content = fin.read()
         fin.close()
         response = 'HTTP/1.1 200 OK\n\n' + content
         client_connection.send(response.encode())
     except FileNotFoundError:
        response = 'HTTP/1.1 404 Not Found\n\nFile Not Found'
        client_connection.sendall(response.encode())
 else:
     response = 'HTTP/1.1 400 Bad Request\n\nRequest Not Supported'

     return response
# Define socket host and port
SERVER_HOST = 'localhost'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)
while True:
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024).decode()
    print('request:\n')
    print(request)

    response = handle_request(request)

    client_connection.sendall(response.encode())
    client_connection.close()
# Close socket
server_socket.close()
