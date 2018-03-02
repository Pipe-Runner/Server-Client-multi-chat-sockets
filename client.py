# This file contains the code for a client.
# It lets you connect to any server socket reachable over your network.
# This code is licenced under open source.

import sys, socket, select

print("Please enter a user name: ")
username = sys.stdin.readline()

def chat_client():
    if(len(sys.argv) < 3) :
        print ('Usage : python chat_client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print ('Unable to connect')
        sys.exit()
    print ('Connected to remote host. You can enter the string to check : : :')
    # sending dummy test to initaiate a chat
    s.send(' ')

    while True:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print ('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('\n'); #changes
                    sys.stdout.flush()

            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(username+'\b'+'>>'+msg)
                #sys.stdout.write('Enter String : '); #ch
                sys.stdout.flush()

if __name__ == "__main__":

    sys.exit(chat_client())
