from server import Server
from control import Control

try: #To catch any errors while execution of code
    host = '192.168.0.100' #Host IP Address
    port = 8080 #Port
    server = Server(host, port) #To establish client-server connection
    controller = Control() #To interface with webcam and motor
    ctr = 0
    running = True
    while running:
        file_name = "images/image{}.jpg".format(ctr)
        controller.capture(file_name) #Take an image from the webcam
        server.send_img(file_name) #Send to compuatational client for processing
        res = server.recv_cmd()
        print(res)
        if res in [0,1]:
            controller.rotate(res) #Control motor action
            print("Biodegradable" if res == 0 else "Non-Biodegradable")
        elif res == 2: #Stop Process
            running = False
        else:
            pass
except Exception as FatalError:
    print(FatalError)

#To clear for next use
server.shutdown()
controller.shutdown()
