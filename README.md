# Face Recognition Attendance System

## Attendence Made Easy

### This is the visual representation of the desktop application.






###Images to the working system can be viewed inside the following directory

- main_directory/system_images/home_page.jpg
- main_directory/system_images/attendence_page.jpg
- main_directory/system_images/attendence_list.jpg
- main_directory/system_images/csv_files.jpg


### Description
The Face Recognition Attendance System is a Python-based application designed to simplify attendance tracking through face recognition. The system utilizes tkinter for the graphical user interface and integrates the face_recognition library for real-time face recognition.

### Features
- **Real-Time Face Recognition:** Utilizes the webcam to perform real-time face recognition.
- **User-Friendly GUI:** A graphical interface with intuitive buttons for attendance control.
- **Date-wise Attendance Storage:** Attendance records are stored in CSV files organized by date.
- **Datetime Module Integration:** Utilizes the datetime module to timestamp attendance records.

### Dependencies
| Packages                       | Versions        |
| ------------------------------ | --------------- |
| pytz                           | Latest          |
| pillow                         | 10.1.0          |
| opencv-python                  | 4.5.4.60        |
| cmake                          | 3.27.7          |
| numpy                          | Latest          |
| face-recognition               | 1.3.0           |
| face-recognition-models        | 0.3.0           |
| distlib                        | 0.3.7           |
| tkinter                        | Latest          |
| customtkinter                  | Latest          |
| csv                            | Included        |

### Process to Run
1. Create a folder on your system to house the project.
2. Inside the folder, create a subfolder for the required images.
3. Place the images of individuals you want to recognize in the images subfolder.
4. Create a Python (.py) file in the main project folder.
5. Run the Python script to execute the Face Recognition Attendance System.
6. The generated CSV file with attendance records will be in the same folder.

### Necessary Changes
- Modify the image paths in the code to reflect the correct location of your images.
- Adjust the GUI coordinates according to your laptop screen size. The provided coordinates are tailored for a 15.6-inch laptop screen.

### Important Notes
- **Microsoft Visual Studio Requirement:** This project requires Microsoft Visual Studio to be installed. The dependency is due to the use of the dlib library for face recognition. Microsoft Visual Studio provides essential components required during the installation of dlib. Please ensure that Microsoft Visual Studio is installed on your system before running the project.
- **Python Version Requirement:** The project is designed to work with Python version 3.8.6. Ensure that your Python installation meets this version requirement.
- **Datetime Module:** The project utilizes the `datetime` module to timestamp attendance records. The module is included in the standard Python library and does not require separate installation.

### Suggestions
- It is recommended to use PyCharm or Visual Studio Code as the preferred code editor for this project.
