import socket
import errno
import termcolor
import random
import sys

HEADERLENGTH = 20
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def msginbyts(message):
    return (f"{len(message):<{HEADERLENGTH}}"+message).encode('utf-8')

def colortext(text, color, attrs = ['bold']):
    return termcolor.colored((text), color, attrs= attrs)

def ask_username():
    while True:
        username = input(colortext("Enter your Username : ", 'blue'))
        if len(username)>3:
            return username
        elif len(username)>0 and len(username)<=3:
            while True:
                weird_username = input(colortext("Are you sure you want to Continue with this Username! ? (yes/no) : ", 'grey'))
                if weird_username in ['yes', 'Yes', 'Y', 'y']:
                    return username
                elif len(weird_username)==0:
                    continue
                else:
                    username = ask_username()
                    return username
        else:
            print(colortext("Invalid Username!", 'red'))
            print(colortext("Please choose a Valid Username to Continue!", 'grey'))

def connecttoserver():
    client_socket.connect(('127.0.0.1', 7547))
    client_socket.setblocking(0)
    client_socket.send(msginbyts(username))

def recvmsg():
    header =  client_socket.recv(HEADERLENGTH)
    if not len(header):
        print('Connection closed by the server')
        sys.exit()
    msg_length = int(header.decode('utf-8').strip())
    return client_socket.recv(msg_length).decode('utf-8')


if __name__ == "__main__":
    username = ask_username()
    try:
        connecttoserver()
        print(colortext("Connected to the Chatting Server!", 'green'))
    except:
        print(colortext("Unable to Connect to the Server!", 'red'))
    while True:
        try:
            message = msginbyts(input(colortext(f"{username} ", 'yellow') + ':>> '))
        except:
            print(colortext("Keyboard Interrupt", 'grey'))
            print(colortext("Exitting the Server", 'red'))
            sys.exit()

        if int(message.decode('utf-8')[:HEADERLENGTH].strip())!=0:
            try:
                client_socket.send(message)
            except:
                print(colortext("Connection from the Server is LOST", 'red'))
                print("Try Connecting again")
                sys.exit()
        else:
            try:
                while True:
                    updates = recvmsg()
                    print(updates)

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                continue

            except Exception as e:
                print('Reading error: '.format(str(e)))
                sys.exit()