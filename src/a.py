import os
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import cv2
import numpy as np


class train:
    def __init__(self, root):  # CONSTRUCTOR CALLED root represents the main Tkinter window
        self.root = root
        self.root.geometry("1530x790+0+0")  # SETTING THE GEOMETRY OF THE WINDOW
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#0a0e27")
        # TITLE LABEL
        title_lbl = Label(
            self.root,
            text="TRAIN DATA SET",
            font=("times new roman", 35, "bold"),
            bg="#130303",
            fg="red",
        )
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(r"..\photos\facw2.png")
        img_top = img_top.resize((1530, 325), Image.LANCZOS)  
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=1530, height=325)
        # TRAIN BUTTON
        b1_1 = Button(
            self.root,
            text="TRAIN DATA",
            command=self.train_classifier,
            cursor="hand2",
            font=("times new roman", 30, "bold"),
            bg="#0a0e27",
            fg="white",
        )
        b1_1.place(x=0, y=380, width=1530, height=60)

        
        
        img_button = Image.open(r"..\photos\face.png")
        img_button = img_button.resize((1530, 325), Image.LANCZOS)  
        self.photoimg_top = ImageTk.PhotoImage(img_button)
        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=440, width=1530, height=325)

        
    def train_classifier(self):
        data_dir = ("data")#DIRECTORY WHERE IMAGES ARE STORED
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]#list comprehension to get image paths

        faces = []
        ids = []#eauta manxe ko lagi eauta id assigned garya hunxa

        for image in path:
            img = Image.open(image).convert("L")  # CONVERTING IMAGE TO GRAYSCALE
            imageNp = np.array(img, "uint8")#grid ma convert garna ko lagi numpy uint8m is data type
            id = int(os.path.split(image)[1].split(".")[1])#getting id from image name 
            #splitting path to get file name and then splitting by . to get id part
            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training", imageNp)
            cv2.waitKey(1) == 13

        ids = np.array(ids)#converting ids list to numpy array

        # TRAIN THE CLASSIFIER AND SAVE
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo(
            "Result", "Training Dataset Completed!", parent=self.root
        )


# =========================== RUN APP ============================
if __name__ == "__main__":
    root = Tk()
    obj = train(root)
    root.mainloop()
