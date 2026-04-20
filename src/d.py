#show the class diagram
#show the sequence diagram for the main flow of the application
#show the sequence diagram for the attendance marking flow      
from tkinter import *
from PIL import Image, ImageTk

class Help:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Help Desk")
        
        # Title
        title_lbl = Label(self.root, text="HELP DESK", font=(
            "times new roman", 35, "bold"), bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        # Main frame with background
        main_frame = Frame(self.root, bg="white")
        main_frame.place(x=0, y=55, width=1530, height=735)
        # Try to load background image, if not available use solid color
        try:
            img_top = Image.open("photos/help.jpg")
            img_top = img_top.resize((1530, 735), Image.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            bg_lbl = Label(main_frame, image=self.photoimg_top)
            bg_lbl.place(x=0, y=0, width=1530, height=735)
        except:
            main_frame.config(bg="#0a0e27") 
        # Help content frame
        content_frame = Frame(main_frame, bg="white", bd=2, relief=RIDGE)
        content_frame.place(x=100, y=50, width=1330, height=
630)
        # Help heading
        help_title = Label(content_frame, text="How Can We Help You?", 
                          font=("times new roman", 28, "bold"), 
                          bg="white", fg="#4a90e2")
        help_title.pack(pady=20)
        # Info frame with scrollbar
        info_frame = Frame(content_frame, bg="white")
        info_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        # Scrollbar
        scrollbar = Scrollbar(info_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Text widget for help content
        self.help_text = Text(info_frame, yscrollcommand=scrollbar.set,
                                font=("Helvetica", 12), bg="white", fg="#333333")
        self.help_text.pack(fill=BOTH, expand=True)



if __name__ == "__main__":
    root = Tk()
    obj = Help(root)
    root.mainloop()
        