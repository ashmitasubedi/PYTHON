import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from tkinter import messagebox
import cv2
import numpy as np
import threading
from datetime import datetime
# ===== FIXED BASE PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)                    # → PYTHON
DATA_DIR = os.path.join(PROJECT_DIR, "data")               

class train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#0a0e27")
        
        # Variables for progress tracking
        self.is_training = False
        self.total_images = 0
        self.processed_images = 0
        
        # Create main canvas with scrollbar
        self.main_canvas = Canvas(self.root, bg="#0a0e27", highlightthickness=0)
        self.main_canvas.place(x=0, y=0, width=1510, height=790)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.main_canvas.yview)
        scrollbar.place(x=1510, y=0, height=790)
        
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create scrollable frame
        self.scrollable_frame = Frame(self.main_canvas, bg="#0a0e27")
        self.canvas_frame = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind mouse wheel scrolling
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.main_canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Compact title
        title_frame = Frame(self.scrollable_frame, bg="#130303", height=45)
        title_frame.pack(fill=X)
        
        title_lbl = Label(
            title_frame,
            text="🎓 TRAIN DATA SET",
            font=("Helvetica", 28, "bold"),
            bg="#130303",
            fg="#00ff88",
        )
        title_lbl.pack(pady=8)
        
        # Compact stats frame
        stats_frame = Frame(self.scrollable_frame, bg="#1a1f3a", relief=RIDGE, bd=2)
        stats_frame.pack(pady=10, padx=40, fill=X)
        
        # Stats container with grid layout
        stats_container = Frame(stats_frame, bg="#1a1f3a")
        stats_container.pack(pady=10)
        
        # Left column stats
        self.total_img_lbl = Label(
            stats_container,
            text="Total Images: 0",
            font=("Arial", 13, "bold"),
            bg="#1a1f3a",
            fg="#00d4ff",
        )
        self.total_img_lbl.grid(row=0, column=0, padx=40, pady=3, sticky=W)
        
        self.processed_img_lbl = Label(
            stats_container,
            text="Processed: 0",
            font=("Arial", 13, "bold"),
            bg="#1a1f3a",
            fg="#ffa500",
        )
        self.processed_img_lbl.grid(row=1, column=0, padx=40, pady=3, sticky=W)
        
        # Right column stats
        self.status_lbl = Label(
            stats_container,
            text="Status: Ready",
            font=("Arial", 13, "bold"),
            bg="#1a1f3a",
            fg="#00ff88",
        )
        self.status_lbl.grid(row=0, column=1, padx=40, pady=3, sticky=W)
        
        self.time_lbl = Label(
            stats_container,
            text="Time: --:--:--",
            font=("Arial", 13, "bold"),
            bg="#1a1f3a",
            fg="#ff69b4",
        )
        self.time_lbl.grid(row=1, column=1, padx=40, pady=3, sticky=W)
        
        # Compact progress bar frame
        progress_frame = Frame(self.scrollable_frame, bg="#1a1f3a", relief=RIDGE, bd=2)
        progress_frame.pack(pady=10, padx=40, fill=X)
        
        Label(
            progress_frame,
            text="Training Progress",
            font=("Arial", 14, "bold"),
            bg="#1a1f3a",
            fg="white",
        ).pack(pady=5)
        
        # Custom styled progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#0a0e27',
            bordercolor='#00ff88',
            background='#00ff88',
            lightcolor='#00ff88',
            darkcolor='#00d4ff',
            thickness=25
        )
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            style="Custom.Horizontal.TProgressbar",
            orient=HORIZONTAL,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10, padx=15, fill=X)
        
        # Content container for preview and controls
        content_container = Frame(self.scrollable_frame, bg="#0a0e27")
        content_container.pack(pady=10, padx=40, fill=BOTH)
        
        # Configure grid columns to be equal width
        content_container.grid_columnconfigure(0, weight=1, uniform="equal")
        content_container.grid_columnconfigure(1, weight=1, uniform="equal")
        
        # Preview frame - Left side
        preview_frame = Frame(content_container, bg="#1a1f3a", relief=RIDGE, bd=2)
        preview_frame.grid(row=0, column=0, padx=8, sticky="nsew")
        
        Label(
            preview_frame,
            text="Live Training Preview",
            font=("Arial", 13, "bold"),
            bg="#1a1f3a",
            fg="#00d4ff",
        ).pack(pady=8)
        
        # Larger preview label with border
        preview_container = Frame(preview_frame, bg="#00d4ff", bd=2, relief=RIDGE)
        preview_container.pack(pady=8, padx=8, fill=BOTH, expand=True)
        
        self.preview_label = Label(preview_container, bg="#0a0e27")
        self.preview_label.pack(fill=BOTH, expand=True, padx=3, pady=3)
        
        # Control panel - Right side
        control_frame = Frame(content_container, bg="#1a1f3a", relief=RIDGE, bd=2)
        control_frame.grid(row=0, column=1, padx=8, sticky="nsew")
        
        Label(
            control_frame,
            text="Training Controls",
            font=("Arial", 15, "bold"),
            bg="#1a1f3a",
            fg="white",
        ).pack(pady=12)
        
        # Compact train button
        self.train_btn = Button(
            control_frame,
            text="🚀 START TRAINING",
            command=self.start_training_thread,
            cursor="hand2",
            font=("Arial", 18, "bold"),
            bg="#00ff88",
            fg="#0a0e27",
            activebackground="#00d4ff",
            activeforeground="white",
            relief=RAISED,
            bd=4,
            padx=15,
            pady=10
        )
        self.train_btn.pack(pady=12)
        
        # Bind hover effects
        self.train_btn.bind("<Enter>", self.on_train_enter)
        self.train_btn.bind("<Leave>", self.on_train_leave)
        
        # Compact info panel
        info_frame = LabelFrame(
            control_frame,
            text="ℹ️ Training Information",
            font=("Arial", 11, "bold"),
            bg="#1a1f3a",
            fg="#00d4ff",
            relief=RIDGE,
            bd=2
        )
        info_frame.pack(pady=12, padx=15, fill=BOTH)
        
        info_text = """• Training uses LBPH Face Recognizer
• Images converted to grayscale
• Saved as 'classifier.xml'
• All 'data' folder images processed
• Use mouse wheel to scroll
• Press ESC to cancel"""
        
        Label(
            info_frame,
            text=info_text,
            font=("Arial", 10),
            bg="#1a1f3a",
            fg="white",
            justify=LEFT
        ).pack(pady=8, padx=8)
        
        # Compact refresh button
        refresh_btn = Button(
            control_frame,
            text="🔄 Refresh Stats",
            command=self.refresh_stats,
            cursor="hand2",
            font=("Arial", 12, "bold"),
            bg="#ffa500",
            fg="white",
            activebackground="#ff8c00",
            relief=RAISED,
            bd=2,
            padx=12,
            pady=6
        )
        refresh_btn.pack(pady=8)
        
        # Compact footer
        footer_frame = Frame(self.scrollable_frame, bg="#130303")
        footer_frame.pack(fill=X, pady=10)
        
        Label(
            footer_frame,
            text="💡 Tip: Use mouse wheel or scrollbar to navigate",
            font=("Arial", 10, "italic"),
            bg="#130303",
            fg="#00d4ff",
        ).pack(pady=8)
        
        # Initial stats refresh
        self.refresh_stats()
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_frame_configure(self, event):
        """Update scroll region when frame size changes"""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Update frame width when canvas size changes"""
        self.main_canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def on_train_enter(self, e):
        if not self.is_training:
            self.train_btn.config(bg="#00d4ff", fg="white")
    
    def on_train_leave(self, e):
        if not self.is_training:
            self.train_btn.config(bg="#00ff88", fg="#0a0e27")
    
    def refresh_stats(self):
        """Refresh statistics about training data"""
        try:
            if os.path.exists(DATA_DIR):
                files = [
                    f for f in os.listdir(DATA_DIR)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
                ]

                self.total_images = len(files)
                self.total_img_lbl.config(text=f"Total Images: {self.total_images}")

                if self.total_images > 0:
                    self.status_lbl.config(text="Status: Ready to Train", fg="#00ff88")
                else:
                    self.status_lbl.config(text="Status: No Images Found", fg="#ff4444")
            else:
                self.total_img_lbl.config(text="Total Images: 0")
                self.status_lbl.config(text="Status: Data Folder Missing", fg="#ff4444")

        except Exception as e:
            print("Error refreshing stats:", e)

    
    def start_training_thread(self):
        """Start training in a separate thread"""
        if not self.is_training:
            self.is_training = True
            self.train_btn.config(
                text="⏸️ TRAINING...",
                state=DISABLED,
                bg="#ff4444"
            )
            thread = threading.Thread(target=self.train_classifier)
            thread.daemon = True
            thread.start()
    
    def update_preview(self, img_array):
        """Update the preview with current training image"""
        try:
            # Get the actual size of the label
            label_width = self.preview_label.winfo_width()
            label_height = self.preview_label.winfo_height()
            
            # Use large size if label dimensions aren't available yet
            if label_width <= 1 or label_height <= 1:
                target_size = 550
            else:
                # Use the smaller dimension to maintain square aspect ratio
                target_size = min(label_width - 10, label_height - 10, 550)
            
            # Resize to large preview size
            img_resized = cv2.resize(img_array, (target_size, target_size))
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(img_pil)
            
            self.preview_label.config(image=img_tk)
            self.preview_label.image = img_tk
        except Exception as e:
            print(f"Preview update error: {e}")
    
    def train_classifier(self):
        try:
            start_time = datetime.now()
            data_dir = DATA_DIR

            
            if not os.path.exists(data_dir):
                messagebox.showerror("Error", "Data folder not found!", parent=self.root)
                self.reset_training_state()
                return
            
            path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) 
                    if file.endswith(('.jpg', '.jpeg', '.png'))]
            
            if len(path) == 0:
                messagebox.showwarning("Warning", "No images found in data folder!", parent=self.root)
                self.reset_training_state()
                return
            
            self.total_images = len(path)
            self.processed_images = 0
            
            faces = []
            ids = []
            
            self.status_lbl.config(text="Status: Training in Progress", fg="#ffa500")
            
            for idx, image in enumerate(path):
                try:
                    img = Image.open(image).convert("L")
                    imageNp = np.array(img, "uint8")
                    id = int(os.path.split(image)[1].split(".")[1])
                    
                    faces.append(imageNp)
                    ids.append(id)
                    
                    self.processed_images = idx + 1
                    progress = (self.processed_images / self.total_images) * 100
                    
                    # Update UI
                    self.progress_bar['value'] = progress
                    self.processed_img_lbl.config(text=f"Processed: {self.processed_images}/{self.total_images}")
                    
                    elapsed = datetime.now() - start_time
                    self.time_lbl.config(text=f"Time: {str(elapsed).split('.')[0]}")
                    
                    # Update preview
                    self.update_preview(imageNp)
                    
                    self.root.update_idletasks()
                    
                except Exception as e:
                    print(f"Error processing image {image}: {e}")
                    continue
            
            if len(faces) == 0:
                messagebox.showerror("Error", "No valid face images found!", parent=self.root)
                self.reset_training_state()
                return
            
            ids = np.array(ids)
            
            # Train and save
            # Train and save
            self.status_lbl.config(text="Status: Saving Classifier...", fg="#00d4ff")
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            clf.write(os.path.join(BASE_DIR, "classifier.xml"))

            
            elapsed = datetime.now() - start_time
            
            self.status_lbl.config(text="Status: Training Complete!", fg="#00ff88")
            messagebox.showinfo(
                "Success",
                f"Training Completed Successfully!\n\nTotal Images: {self.processed_images}\nTime Taken: {str(elapsed).split('.')[0]}",
                parent=self.root
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}", parent=self.root)
            self.status_lbl.config(text="Status: Training Failed", fg="#ff4444")
        
        finally:
            self.reset_training_state()
    
    def reset_training_state(self):
        """Reset UI after training"""
        self.is_training = False
        self.train_btn.config(
            text="🚀 START TRAINING",
            state=NORMAL,
            bg="#00ff88",
            fg="#0a0e27"
        )
        

# =========================== RUN APP ============================
if __name__ == "__main__":
    root = Tk()
    obj = train(root)
    root.mainloop()