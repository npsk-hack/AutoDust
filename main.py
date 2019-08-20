from tkinter import *
from PIL import Image, ImageTk
import cv2
from Capture import *
from receiver import *
import socket
import ImageClassifier
import time

s = time.time()

receive_image() #calls upon the receiver.py file to receive the server-sent image

clf = ImageClassifier.ObjectDetection() #creates an instance of the ObjectDetection class in the ImageClassifier.py file
temp_image = clf.load() 
result = clf.classify(temp_image)

image = result['image_data'] #returns the cv2 object of the classified image

tup = CaptureProcess(result['detections']) #returns a tuple containing the detected object and it's corresponding key value
obj = tup[0]
val = tup[1]

#creates the frontend display 
main = Tk()
main.attributes('-fullscreen', True)
main.title("AutoDust Server")
main.configure(bg='light cyan')
fnt = ('Courier New', 35, "bold")
head = Label(main, text="AUTODUST", font=fnt, bg='light cyan', fg='navy')
head.grid(row=0, column=0, columnspan=5, padx=570, pady=30)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img = Image.fromarray(image)
img = img.resize((750, 500), Image.ANTIALIAS)
tk_image = ImageTk.PhotoImage(img)
image = Label(main, image=tk_image, width=750, height=500, bg="black")
image.grid(row=1, column=0, padx=0, pady=30, rowspan=7)

txt2 = Label(main, text='RESULT:-', font=('Courier New', 20, "bold"), bg='light cyan', fg='navy')
txt2.grid(row=1,column=1)

if len(obj)!=0:
    st=""
    for i in obj.split(" "):
        st += (i.capitalize() + " ")
else:
    st = "No Waste"
    
detect = 'Detected Waste: {}'.format(st)
txt3 = Label(main, text=detect, font=('Courier New', 20), bg='light cyan', fg='navy')
txt3.grid(row=2, column=1)

if len(obj)!=0:
    if val==0:
        f = "BioDegrabdable"
    else:
        f = "Non-BioDegradable"
else:
    f = "-N/A-"
    
result = 'Waste Type:- {}'.format(f)
txt4 = Label(main, text=result, font=('Courier New', 20), bg='light cyan', fg='navy')
txt4.grid(row=3, column=1, padx=0)

#sends the server file AutoDust.py the following data
if len(str(val))>0:
    conn.send(str(val).encode('utf-8'))
else:
    conn.send(b'2')

r = time.time()
runtime = r-s #returns the runtime for the project
txt5 = Label(main, text='Runtime: {}'.format(round(runtime,3)), font=('Courier New', 20), bg='light cyan', fg='navy')
txt5.grid(row=4, column=1, padx=0)

print(runtime)
main.mainloop()
