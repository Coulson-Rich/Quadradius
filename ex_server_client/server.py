import socket
import _thread
import sys

server = "IPV4 ADDRESS"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
s.listen(2)
print("Waiting for a connection, Server Started")

pos = [(0,0),(100,100)]

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def threaded_client(conn, currPlayer):
    conn.send(str.encode(make_pos(pos[currPlayer])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[currPlayer] = data

            if not data:
                print("Disconnected")
                break
            else:
                if currPlayer == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending : ", reply)
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print("Lost connection")
    conn.close()
currPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    _thread.start_new_thread(threaded_client, (conn,currPlayer))
    currPlayer += 1
