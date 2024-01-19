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
from PIL import ImageTk, Image
import customtkinter

class FaceRecognitionApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x640")
        self.master.title("Face Recognition Attendance System")

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        self.selected_csv_file = None

        self.setup_ui()

    def setup_ui(self):
        img1 = ImageTk.PhotoImage(Image.open("pattern.png"))
        self.l1 = customtkinter.CTkLabel(master=self.master, image=img1)
        self.l1.pack()

        self.frame = customtkinter.CTkFrame(master=self.l1, width=500, height=450, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        l2 = customtkinter.CTkLabel(master=self.frame, text="ATTENDANCE MADE EASY", font=('Century Gothic', 20, 'bold'))
        l2.place(x=135, y=45)

        self.start_button = customtkinter.CTkButton(master=self.frame, width=200, height=50, text="Start Attendance",
                                               corner_radius=10, font=('Arial', 16), command=self.start_attendance)
        self.start_button.place(x=40, y=150)

        self.stop_button = customtkinter.CTkButton(master=self.frame, width=200, height=50, text="Stop Attendance",
                                              corner_radius=10, font=('Arial', 16), command=self.stop_attendance)
        self.stop_button.place(x=270, y=150)

        self.label_combobox = customtkinter.CTkLabel(master=self.frame, text="Attendance Files:", font=('Arial', 20, 'bold'))
        self.label_combobox.place(x=65, y=250)

        self.attendance_list_combobox = ttk.Combobox(master=self.frame, width=12, height=40, font=('Arial', 12))
        self.attendance_list_combobox['values'] = ("Option 1", "Option 2", "Option 3")  # Example values
        self.attendance_list_combobox.set("Select")  # Set default value
        self.attendance_list_combobox.place(x=230, y=250)
        self.attendance_list_combobox.bind("<<ComboboxSelected>>", self.on_csv_dropdown_selected)
        self.attendance_list_combobox.bind("<FocusOut>", self.reset_combobox)

        self.update_csv_dropdown()

        self.open_button = customtkinter.CTkButton(master=self.frame, width=60, height=28, text="Open",
                                                   corner_radius=6, font=('Arial', 12), command=self.open_selected_csv_file)
        self.open_button.place(x=365, y=248)

        # Bind button events
        self.start_button.bind("<Enter>", self.on_enter)
        self.start_button.bind("<Leave>", self.on_leave)

        self.stop_button.bind("<Enter>", self.on_enter)
        self.stop_button.bind("<Leave>", self.on_leave)   
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.master.mainloop()
    
    def reset_combobox(self, event):
        self.attendance_list_combobox.set("Select")

    def on_click(self, event, button_name):
        if button_name == "Start":
            self.start_attendance()
        elif button_name == "Stop":
            self.stop_attendance()

    def on_enter(self, event):
        if event.widget.cget('state') == 'active':
            event.widget.configure(bg='#16a085')  # Clicked color

    def on_leave(self, event):
        event.widget.configure(bg='Ba4a00')

    def on_closing(self):
        if hasattr(self, 'video_capture') and self.video_capture is not None:
            self.stop_attendance()
        self.master.destroy()

    def start_attendance(self):
        self.video_capture = cv2.VideoCapture(0)
        self.stop_event = False
        self.thread = Thread(target=self.attendance_thread)
        self.thread.start()

    def stop_attendance(self):
        if hasattr(self, 'video_capture') and self.video_capture is not None:
            self.stop_event = True
            self.thread.join()  # Wait for the thread to finish
            self.video_capture.release()
            cv2.destroyAllWindows()
            self.video_capture = None

    def update_csv_dropdown(self):
         # Fetch the list of CSV files in the directory for attendance list
        csv_files = [f for f in os.listdir() if f.endswith(".csv")]
        self.attendance_list_combobox['values'] = csv_files

    def on_csv_dropdown_selected(self, event):
        self.selected_csv_file = self.attendance_list_combobox.get()

    def open_selected_csv_file(self):
        if self.selected_csv_file:
            try:
                subprocess.Popen(["start", "excel", self.selected_csv_file], shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open file: {str(e)}")

    def attendance_thread(self):
        # For demonstration purposes, I'm leaving the face recognition logic as in your provided code
        aastha_image = face_recognition.load_image_file(r"D:\DesktopApp\photos\aastha.jpeg")
        aastha_encoding = face_recognition.face_encodings(aastha_image)[0]

        tesla_image = face_recognition.load_image_file(r"D:\DesktopApp\photos\tesla.jpeg")
        tesla_encoding = face_recognition.face_encodings(tesla_image)[0]
        
        known_face_encoding = [aastha_encoding, tesla_encoding]
        known_faces_names = ["Aastha", "Tesla"]

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

                cv2.imshow("Attendence System", frame) # display the video feed.
                if cv2.waitKey(1) & 0xFF == ord('q'): #if key is q then its terminated.
                    break
                
        cv2.destroyAllWindows()
        f.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
