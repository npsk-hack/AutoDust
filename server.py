from time import time as cur
import socket

class Server:
    def __init__(self, host='', port=8080):
        self.host = host
        self.port = port
        self.serv = socket.socket()
        self.serv.bind((host, port)) #Create a server
        self.serv.listen(3)
        print("Server {} listening on port {}".format(host, port))
        self.conn, self.client = self.serv.accept() #Connect to client
        print("Connected to {} on port {}".format(self.client[0], self.client[1]))

    def send_img(self, file_name = ''):
        with open(file_name, 'rb+') as file:
            img_data = file.read()
        sz = len(img_data)
        self.conn.send(str(sz).encode('UTF-8'))
        self.conn.recv(1)
        pack_size = 2048 #To compensate for WiFi limitations
        start = cur()
        ind = 0
        while ind < sz:
            self.conn.send(img_data[ind:ind+pack_size])
            self.conn.recv(1)
            ind += pack_size
        self.conn.send(img_data[ind:])
        print('Image sent')
        stop = cur()
        print('Time Taken: {}s'.format(round(stop-start, 2)))

    def recv_cmd(self):
        res = int(self.conn.recv(1).decode())
        self.conn.send(b'1')
        return res

    def shutdown(self):
        self.serv.shutdown(socket.SHUT_RDWR) #To Shutdown server
        self.serv.close()
        print("Server Disabled")
