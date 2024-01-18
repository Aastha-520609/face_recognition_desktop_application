import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
import csv
from datetime import datetime
import cv2
import face_recognition
import numpy as np
import os
import subprocess

class FaceRecognitionAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Set the background color of the frame
        self.root.configure(bg="#34495E")

        # Create a style for buttons
        style = ttk.Style()
        style.configure("TButton",
                        padding=10,
                        font=('Helvetica', 14),
                        background='#3498db',
                        foreground='#ffffff',
                        borderwidth=2,
                        relief="groove")

        # Create a frame for better organization
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Create a label for the heading
        heading_label = ttk.Label(self.frame, text="Face Recognition Attendance Management System",
                                font=('Helvetica', 18), background="#34495E", foreground="#ffffff")
        heading_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Create buttons
        self.start_button = ttk.Button(self.frame, text="Start Attendance", command=self.start_attendance)
        self.stop_button = ttk.Button(self.frame, text="Stop Attendance", command=self.stop_attendance)

        self.attendance_list_button = ttk.Button(self.frame, text="Attendance List",  command=self.show_attendance_list)
        #self.attendance_list_dropdown = ttk.Combobox(self.frame, textvariable=self.selected_csv_file, state="readonly")
        self.selected_csv_file = tk.StringVar()
        self.csv_dropdown = ttk.Combobox(self.frame, textvariable=self.selected_csv_file, state="readonly")
        self.csv_dropdown.bind("<<ComboboxSelected>>", self.on_csv_dropdown_selected)


        # Set button positions
        self.start_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.stop_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        #self.attendance_list_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.attendance_list_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        self.csv_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        # Bind button events
        self.start_button.bind("<Enter>", self.on_enter)
        self.start_button.bind("<Leave>", self.on_leave)

        self.stop_button.bind("<Enter>", self.on_enter)
        self.stop_button.bind("<Leave>", self.on_leave)   
         
        self.attendance_list_button.bind("<Enter>", self.on_enter)
        self.attendance_list_button.bind("<Leave>", self.on_leave)

        self.update_csv_dropdown()


        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_csv_dropdown(self):
         # Fetch the list of CSV files in the directory for attendance list
        csv_files= [f for f in os.listdir() if f.endswith(".csv")]
        self.csv_dropdown["values"] = csv_files
    
    def on_csv_dropdown_selected(self, event):
        selected_csv_file = self.selected_csv_file.get()
        if selected_csv_file:
            # Do something with the selected CSV file (e.g., open it)
            try:
                subprocess.Popen(["start", "excel", selected_csv_file], shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open file: {str(e)}")

    def on_enter(self, event):
        event.widget.configure(background='#2980b9')

    def on_leave(self, event):
        event.widget.configure(background='#3498db')

    def on_closing(self):
        if hasattr(self, 'video_capture') and self.video_capture is not None:
            self.stop_attendance()
        self.root.destroy()
    
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
        if hasattr(self, 'video_capture') and self.video_capture is not None: #if self.video_capture is not None:
            self.stop_event = True
            self.thread.join()  # Wait for the thread to finish
            self.video_capture.release()
            cv2.destroyAllWindows()
            self.video_capture = None
        
    def show_attendance_list(self):
        selected_csv_file = self.selected_csv_file.get()
        if selected_csv_file:
            with open(selected_csv_file, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    print(row)
        self.update_csv_dropdown()            
    
    def attendance_thread(self):
        aastha_image = face_recognition.load_image_file(r"D:\DesktopApp\photos\aastha.jpeg")
        aastha_encoding = face_recognition.face_encodings(aastha_image)[0]

        tesla_image = face_recognition.load_image_file(r"D:\DesktopApp\photos\tesla.jpeg")
        tesla_encoding = face_recognition.face_encodings(tesla_image)[0]
        
        known_face_encoding = [aastha_encoding, tesla_encoding]
        known_faces_names = ["aastha", "tesla"]

        students = known_faces_names.copy()

        face_locations = []
        face_encodings = []
        face_names = []

        s = True

        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")

        f = open(current_date + '.csv', 'w+', newline='')
        lnwriter = csv.writer(f)
        
        while not self.stop_event:
            ret, frame = self.video_capture.read() #captures video frames from the webcam.
            if ret:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) #resizes the captured frame in smaller size making it more
                #efficient for face recognition procesing.
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB) #converts the resized frame from default BGR to RGB
                #which is the format expected by face recognition library.
                if s:
                    #detected faces location and encodings are stored.
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) #images are encoded.
                    face_names = []
                    #processes each detected face, compares it with known faces, and updates the attendance status.
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(known_face_encoding, face_encoding) #Compares the current face encoding with the known face encodings stored in known_face_encoding
                        name = ""
                        face_distance = face_recognition.face_distance(known_face_encoding, face_encoding) #Calculates the face distance (similarity) between the current face encoding and known face encodings.
                        best_match_index = np.argmin(face_distance) # Finds the index of the smallest face distance, indicating the best match.

                        if matches[best_match_index]:
                            name = known_faces_names[best_match_index] #name is assigned from known_faces_names
                        face_names.append(name)

                        if name in known_faces_names:
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            bottomLeftCornerOfText = (10, 100)
                            fontScale = 1.5
                            fontColor = (255, 0, 0)
                            thickness = 3
                            lineType = 2

                            #shows text on the video feed which includes name of the student(jpg) and present.
                            #helps us to show real time results.
                            cv2.putText(frame, name + ' Present', #putText helps to mark the attendence
                                        bottomLeftCornerOfText,
                                        font,
                                        fontScale,
                                        fontColor,
                                        thickness,
                                        lineType)

                            if name in students:
                                students.remove(name)
                                print(students)
                                current_time = now.strftime("%H-%M-%S")
                                lnwriter.writerow([name, current_time]) #written to csv file.

                cv2.imshow("attendence system", frame) # display the video feed.
                if cv2.waitKey(1) & 0xFF == ord('q'): #if key is q then its terminated.
                    break
                
        cv2.destroyAllWindows()
        f.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    app = FaceRecognitionAppGUI(root)
    root.mainloop()
