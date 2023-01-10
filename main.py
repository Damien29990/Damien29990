import socket
import threading
import time

def creat_response (clientsocket, address):

    while True:
        try:
            message = clientsocket.recv(1024).decode()

            if not message:
                print("No message recieved, closing client connection...")
                clientsocket.close()
                break

            try:
                headers = message.split('\n')
                fields = headers[0].split()
                request_type = fields[0]
                filename = fields[1]
                print ('Type: %s and File: %s' % (request_type, filename))
                

            except Exception as e:
                print("Error getting request method/http version/message")
                retype = "400 Bad Request"
                response = 'HTTP/1.1 400 Bad Request\n\nRequest Not Supported'
                clientsocket.send(response.encode())
                print("Closing client socket...")
                clientsocket.close()
                break

            if request_type == "GET":
                try:
                    if filename == '/':
                        filename = '/index.html'
                        
                    filetype = filename.split('.')[1]
                except Exception as e:
                    print("Error getting filetype/requested file")
                    print("Closing client socket...")
                    clientsocket.close()
                    break
            else:
                print("Error getting request method/http version/message")
                retype = "400 Bad Request"
                response = 'HTTP/1.1 400 Bad Request\n\nRequest Not Supported'
                clientsocket.send(response.encode())
                print("Closing client socket...")
                clientsocket.close()
                break

            if filetype == "html":
                print("correct type of request")
                try:
                    
                    print(filename)
                    fin = open('/python' + filename)
                    content = fin.read()
                    fin.close()
                    retype = "200 OK"
                    response = 'HTTP/1.1 200 OK\n\n' + content
                    clientsocket.send(response.encode())
                except FileNotFoundError:
                    retype = "404 Not Found"
                    response = 'HTTP/1.1 404 Not Found\n\nFile Not Found'
                    clientsocket.send(response.encode())
                    break
            elif filetype == "jpg" or filetype == "jpeg" or filetype == "png":
                try:
                    
                    print(filename)
                    fin = open('/python' + filename, 'rb')
                    content = fin.read()
                    fin.close()
                    retype = "200 OK"
                    response = 'HTTP/1.1 200 OK\n\n'
                    clientsocket.send(response.encode())
                    clientsocket.send(content)
                except FileNotFoundError:
                    retype = "404 Not Found"
                    response = 'HTTP/1.1 404 Not Found\n\nFile Not Found'
                    clientsocket.send(response.encode())
                    break
            log = open("log.txt", mode='a')
            log.write("\nThread no: "+str(Threadcount))
            log.write("\nIP address: "+str(address))
            log.write("\nFilename: "+str(filetype))
            log.write("\nResponse type: "+retype)
            log.close()

            
        except socket.timeout:
            print("Timeout")
            clientsocket.close()
            break

 
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("socket successfully created")
log = open("log.txt", mode='w')
log.close()
print ("Log file successfully created")

serverport = 80
Threadcount = 0

serversocket.bind(('',serverport))
print ("socket binded to %s" %(serverport))

serversocket.listen(1)
print('Listening on port %s ...' %(serverport))

while True:
    clientsocket, address = serversocket.accept()
    print('Got connection from',address,'\n')
    threading.Thread(target=creat_response, args=(clientsocket,address)).start()
    Threadcount += 1
