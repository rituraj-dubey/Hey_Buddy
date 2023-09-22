import socket
import select
import termcolor

HEADERLENGTH = 20
server_ip = "127.0.0.1"
server_port = 7547
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((server_ip, server_port))
server_socket.listen()

sockets_list = [server_socket]
clients = {}

def colorit(text, color, attrs= ['bold']):
    return termcolor.colored((text), color, attrs = attrs)

print(colorit("Server is ONLINE at ",'red', attrs= ['bold', 'blink']) + 
      colorit(f"{server_ip} : ", 'green', attrs = ['bold', 'blink']) 
      + colorit(f"{server_port}", 'blue', attrs= ['bold', 'blink']))

def recv_message(client_socket):
    try:
        message_header = client_socket.recv(HEADERLENGTH)

        if not len(message_header):
            return False
        
        message_length = int(message_header.decode('utf-8').strip())
        
        return {'header': message_length, 'data': client_socket.recv(message_length).decode('utf-8')}
    except:
        return False

while True:
    read_lt,_,exception_lt = select.select(sockets_list,[],sockets_list)

    for notified_socket in read_lt:
        if notified_socket == server_socket:
            client_socket , client_address = server_socket.accept()
            user = recv_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(colorit(f"Accepted new Connection from {client_address[0]} : {client_address[1]}, username : {user['data']}", 'green'))

        else:
            message = recv_message(notified_socket)
            if message is False:
                print(colorit('Closed connection from: {}'.format(clients[notified_socket]['data']), 'red'))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(colorit(f"Recieved Message from {user['data']} : {message['data']}", 'blue'))

            for client_socket in clients:
                if client_socket != notified_socket:
                    message = f"{user['header']+message['header']+5:<{HEADERLENGTH}}" + f"{user['data']} ::> {message['data']}"
                    client_socket.send(message.encode('utf-8'))

    for notified_socket in exception_lt:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]