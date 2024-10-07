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

# Global Variables:
**gaze_data:** Stores the gaze data collected during the session.
**new_frame:** Stores the updated video frame (used in gaze tracking and image blending).
**coordinates_folder:** Folder path where Excel files with gaze data are saved.

# Functions:
**1. update_new_frame(frame)**
This function updates the global new_frame variable with the new frame captured from the webcam, which will be used later for display.

**2. on_close()**
This function handles the closing of the Tkinter window, prompting the user for confirmation before quitting the application.

**3. start_detection()**
This is the main function where the gaze tracking starts. Here's what it does:

**User Prompt:** It first creates a UserInformationDialog to prompt the user for their personal information (ID, name, age, gender, city, socio-economic class, brand).
**Gaze Tracking Setup:** Initializes the GazeTracking object and webcam.
**Image Loading:** Loads an image (biscuit.jpg) which is displayed alongside the real-time webcam feed during gaze detection.
**Gaze Detection Loop:** Runs for 30 seconds, capturing webcam frames and detecting the user's gaze coordinates (horizontal and vertical ratios).
**Display and Blending:** Blends the webcam frame and the image, displaying it in fullscreen mode. The gaze coordinates are displayed at the bottom center of the window.
**Data Storage:** After 30 seconds, the gaze data (X and Y coordinates) along with the timestamp is stored in a pandas DataFrame, which is then exported as an Excel file.
**4. UserInformationDialog (Class)**
This class is responsible for collecting user information via a Tkinter pop-up dialog. The collected details include:

ID (numeric),
Name (text),
Age (dropdown: 09-12, 13-19, 20-30),
Gender (dropdown: Male, Female),
City (dropdown: Karachi, Lahore, Multan, Faisalabad),
Socio-Economic Class (SEC's) (dropdown: SEC-A, SEC-B, SEC-C, SEC-D),
Brand Preference (dropdown: Lemon Sandwich, Chocolate Sandwich, RIO Double Chocolate, Prince, Oreo).
Upon completion, the dialog passes the entered user information back to the start_detection() function.

# Tkinter Window:
**Main Window:** A basic Tkinter window is created with a "Start Detection" button that calls the start_detection() function when clicked.

# How the Gaze Detection Works:
**GazeTracking Library:** This library estimates the user's gaze direction by calculating horizontal and vertical gaze ratios. It provides the method horizontal_ratio() and vertical_ratio() to get normalized coordinates, where:

A ratio of 0 means the user is looking to the far left/top.
A ratio of 1 means the user is looking to the far right/bottom.
Image Blending: The real-time webcam feed is blended with a static image (biscuit.jpg). The cv2.addWeighted() function combines the two images using an alpha blending factor (0.9 in this case).

Displaying Gaze Coordinates: The gaze coordinates (X and Y) are displayed as text on the blended image, and the result is shown in fullscreen mode using OpenCV.

# Data Export:
Once the gaze tracking process completes (after 30 seconds), the captured data is stored in an Excel file. The data includes:

ID: User's ID.
Name: User's name.
Age: User's age group.
Gender: User's gender.
City: The city the user belongs to.
SEC's: Socio-Economic Class.
Brand: The brand chosen by the user.
Timestamp: The timestamp of when each gaze coordinate was captured.
Gaze X and Gaze Y: The horizontal and vertical gaze coordinates.
The Excel file is saved in a folder named COORDINATES, with the filename format as {user_id}_{name}.xlsx.
