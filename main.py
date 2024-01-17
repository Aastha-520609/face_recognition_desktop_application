import tkinter as tk
from tkinter import ttk
from threading import Thread
import csv
from datetime import datetime
import cv2
import face_recognition
import numpy as np

class FaceRecognitionAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.video_capture = None
        self.thread = None
        self.stop_event = None

        # Set the background color of the frame
        self.root.configure(bg="#2C3E50")

        # Create a style for buttons
        style = ttk.Style()
        style.configure("TButton",
                        padding=10,
                        font=('Helvetica', 14),
                        background='#3498db',
                        foreground='#ffffff')

        # Create buttons
        self.start_button = ttk.Button(root, text="Start Attendance", command=self.start_attendance)
        self.stop_button = ttk.Button(root, text="Stop Attendance", command=self.stop_attendance)
        self.list_button = ttk.Button(root, text="Attendance List", command=self.show_attendance_list)

        # Set button positions
        self.start_button.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='ew')
        self.stop_button.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='ew')
        self.list_button.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')

        # Make buttons respond to hover and click events
        self.start_button.bind("<Enter>", self.on_enter)
        self.start_button.bind("<Leave>", self.on_leave)
        self.start_button.bind("<Button-1>", lambda event: self.on_click(event, "Start"))

        self.stop_button.bind("<Enter>", self.on_enter)
        self.stop_button.bind("<Leave>", self.on_leave)
        self.stop_button.bind("<Button-1>", lambda event: self.on_click(event, "Stop"))

        self.list_button.bind("<Enter>", self.on_enter)
        self.list_button.bind("<Leave>", self.on_leave)
        self.list_button.bind("<Button-1>", lambda event: self.on_click(event, "List"))

    def on_enter(self, event):
        event.widget.configure(background='#2980b9')

    def on_leave(self, event):
        event.widget.configure(background='#3498db')

    def on_click(self, event, button_name):
        if button_name == "Start":
            self.start_attendance()
        elif button_name == "Stop":
            self.stop_attendance()
        elif button_name == "List":
            self.show_attendance_list()

    def start_attendance(self):
        self.video_capture = cv2.VideoCapture(0)
        self.stop_event = False
        self.thread = Thread(target=self.attendance_thread)
        self.thread.start()

    def stop_attendance(self):
        if self.video_capture:
            self.stop_event = True
            self.thread.join()  # Wait for the thread to finish
            self.video_capture.release()
            cv2.destroyAllWindows()

    def show_attendance_list(self):
        print("Showing Attendance List")

    def attendance_thread(self):
        known_faces_names = ["aastha", "tesla"]
        known_face_encoding = []

        aastha_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\ethics\photos\aastha.jpeg")
        tesla_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\ethics\photos\tesla.jpeg")

        known_face_encoding.extend([
            face_recognition.face_encodings(aastha_image)[0],
            face_recognition.face_encodings(tesla_image)[0]
        ])

        students = known_faces_names.copy()

        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")

        f = open(current_date + '.csv', 'w+', newline='')
        lnwriter = csv.writer(f)

        while not self.stop_event:
            _, frame = self.video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Face recognition logic
            # ... (same as in the previous code)

            cv2.imshow("attendance system", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        f.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    app = FaceRecognitionAppGUI(root)
    root.mainloop()


""" import tkinter as tk
from tkinter import ttk

class FaceRecognitionAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")

        # Set the background color of the frame
        self.root.configure(bg="#2C3E50")

        # Create a style for buttons
        style = ttk.Style()
        style.configure("TButton",
                        padding=10,
                        font=('Helvetica', 14),
                        background='#3498db',
                        foreground='#ffffff')

        # Create buttons
        self.start_button = ttk.Button(root, text="Start Attendance", command=self.start_attendance)
        self.stop_button = ttk.Button(root, text="Stop Attendance", command=self.stop_attendance)
        self.list_button = ttk.Button(root, text="Attendance List", command=self.show_attendance_list)

        # Set button positions
        self.start_button.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='ew')
        self.stop_button.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='ew')
        self.list_button.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')

        # Make buttons respond to hover and click events
        self.start_button.bind("<Enter>", self.on_enter)
        self.start_button.bind("<Leave>", self.on_leave)
        self.start_button.bind("<Button-1>", lambda event: self.on_click(event, "Start"))

        self.stop_button.bind("<Enter>", self.on_enter)
        self.stop_button.bind("<Leave>", self.on_leave)
        self.stop_button.bind("<Button-1>", lambda event: self.on_click(event, "Stop"))

        self.list_button.bind("<Enter>", self.on_enter)
        self.list_button.bind("<Leave>", self.on_leave)
        self.list_button.bind("<Button-1>", lambda event: self.on_click(event, "List"))

    def on_enter(self, event):
        event.widget.configure(background='#2980b9')

    def on_leave(self, event):
        event.widget.configure(background='#3498db')

    def on_click(self, event, button_name):
        print(f"Button clicked: {button_name}")

    def start_attendance(self):
        # Implement the functionality for starting attendance here
        print("Starting Attendance")

    def stop_attendance(self):
        # Implement the functionality for stopping attendance here
        print("Stopping Attendance")

    def show_attendance_list(self):
        # Implement the functionality for showing attendance list here
        print("Showing Attendance List")


if __name__ == "__main__":
    root = tk.Tk()

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the dimensions of the GUI to cover the entire screen
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    app = FaceRecognitionAppGUI(root)
    root.mainloop()
 """