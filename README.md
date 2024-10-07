# Eye_Tracking
This Python program captures real-time gaze data using a webcam and the GazeTracking library. The user is prompted to enter their personal details through a GUI built with Tkinter, and gaze data is collected over a set period of time (30 seconds). The gaze data, along with the user information, is then saved to an Excel file for further analysis.

# Libraries and Modules:
1. cv2 (OpenCV): Used for capturing video from the webcam and manipulating image frames.
2. GazeTracking: A library to detect the user's gaze and estimate the coordinates.
3. pandas: For handling and storing data in DataFrames and exporting them to Excel.
4. time: For measuring the timestamp of gaze data.
5. os: For file handling and directory management.
6. tkinter: For building the graphical user interface (GUI) and handling user input.
7. ttk: Tkinter's themed widgets (Combobox for dropdowns).
8. numpy: Used for numerical operations, although it's not explicitly used in this code.
9. matplotlib and seaborn: These libraries are imported but not used in the given code.
