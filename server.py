# chat_server.py
 
import sys, socket, select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9099
sock_list = []
stored = []

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print ("Client chat started on "+ str(PORT))
 
    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        for sock in ready_to_read:

            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print ("Client (%s, %s) connected" % addr)
                 
                #reply(server_socket, sockfd, "[%s:%s] entered our palindrome checker\n" % addr)
             
            # a message from a client, not a new connection
            else:
                if sock not in sock_list:
                    sock_list.append(sock)
                    for text in stored:
                        reply(server_socket,sock,text+'\n')

                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        stored.append(data)
                        for x in sock_list:
                            if( x != sock ):
                                reply(server_socket, x,data)
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        reply(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    reply(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()
    

def reply (server_socket, sock, message):
    # for socket in SOCKET_LIST:
    socket=sock
        # send the message only to peer
    if socket != server_socket:
        try :
            message=message.strip()
            socket.send(message+'\n')
        except :
                # broken socket connection
            socket.close()
                # broken socket, remove it
            if socket in SOCKET_LIST:
                SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())


         
