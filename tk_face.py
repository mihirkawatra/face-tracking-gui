import numpy as np
import cv2
import tkinter as tk
from PIL import Image,ImageTk
import os
import datetime

face_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__))+'/resources/haarcascade_frontalface_default.xml')
ss = 0

def screenshot():
    global ss
    ss=1

window = tk.Tk()
window.wm_title("Face Tracking")
window.config(background="#878787")

imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,960)
ret,frame = cap.read()
def show_frame():
    global ss
    ret, frame = cap.read()
    frame = cv2.flip(frame, flipCode=1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    image_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    for (x,y,w,h) in faces:
        cv2.rectangle(image_rgba,(x,y),(x+w,y+h),(255,255,0),thickness=2)
    img = Image.fromarray(image_rgba)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

    if ss == 1:
        if faces!=():
            filename = "{}.png".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            img = Image.fromarray(image_rgba[y:y+h, x:x+w])
            img.save(filename)
            print("[INFO] saved {}".format(filename))
        ss=0

#Slider window (slider controls stage position)
#sliderFrame = tk.Frame(window, width=600, height=100)
#sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

capture = tk.Button(window, text="Capture", fg="Black",bg="Red", command=screenshot)
capture.grid(row=2,column=0,columnspan=2,sticky=tk.W,padx=200,pady=40)

exit = tk.Button(window, text="Exit", fg="Black", bg="Red", command=window.destroy)
exit.grid(row=2,column=0,columnspan=2,sticky=tk.E,padx=200,pady=40)

show_frame()  #Display 2
window.mainloop()  #Starts GUI
