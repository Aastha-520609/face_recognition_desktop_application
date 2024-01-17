
import csv
from datetime import datetime
import cv2
import face_recognition
import numpy as np

#sets up the webcam for capturing video.
video_capture = cv2.VideoCapture(0) #signifies the code is using the default camera for capturing.

#himanshu_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\ethics\photos\himanshu.jpeg") #imgs are loaded
#himanshu_encoding = face_recognition.face_encodings(himanshu_image)[0] # generates face encodings(vectors representing faical features) are loaded

aastha_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\ethics\photos\aastha.jpeg")
aastha_encoding = face_recognition.face_encodings(aastha_image)[0]

tesla_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\ethics\photos\tesla.jpeg")
tesla_encoding = face_recognition.face_encodings(tesla_image)[0]

#ramraj_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\ethics\photos\ramraj.jpeg")
#ramraj_encoding = face_recognition.face_encodings(ramraj_image)[0]

#A list containing - face encodings for known individuals.
known_face_encoding = [
    #himanshu_encoding,
    aastha_encoding,
    tesla_encoding,
    #ramraj_encoding
]

#A list containing - corresponding names for known individuals.
known_faces_names = [
    #"himanshu",
    "aastha",
    "tesla",
    #"ramraj"
]

# A copy of the list of known faces' names, used for tracking attendance.
students = known_faces_names.copy()

#Lists to store face detection results.
face_locations = []
face_encodings = []
face_names = []

# A boolean variable used to control certain actions (e.g., printing students and writing to CSV).
s = True

now = datetime.now() # Gets the current date and time.
current_date = now.strftime("%Y-%m-%d")  #strftime - used to format time in YYYY-MM-DD

f = open(current_date + '.csv', 'w+', newline='') #opens or create a csv file with the current date as file name
lnwriter = csv.writer(f) #creating a writer object and writing rows of data into f file

while True:
    _, frame = video_capture.read() #captures video frames from the webcam.
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

video_capture.release() #Release the webcam resources.
cv2.destroyAllWindows() #closes all opencv windows.
f.close() # close the csv file.
