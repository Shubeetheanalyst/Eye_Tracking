#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import cv2
from gaze_tracking import GazeTracking
import pandas as pd
import time
import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Global variables to store the gaze data and the path to the saved Excel file
gaze_data = None
new_frame = None  # Declare new_frame as a global variable
coordinates_folder = "COORDINATES"  # Folder to store Excel files

# Function to update the new_frame
def update_new_frame(frame):
    global new_frame
    new_frame = frame

def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def start_detection():
    global gaze_data, new_frame  # Use the global new_frame
    gaze_data = None

    # Prompt for user information
    user_info = UserInformationDialog(root)
    root.wait_window(user_info.top)

    if not user_info.cancelled:
        user_id, name, age, gender, city, sec, brand = user_info.get_user_info()

        gaze = GazeTracking()
        webcam = cv2.VideoCapture(0)

        start_time = time.time()

        # Load the image without resizing (using the uploaded image file path)
        img = cv2.imread("biscuit.jpg")

        # Ensure the image is not None and get its dimensions
        if img is None:
            print("Error: Image not found.")
            exit()
        img_height, img_width = img.shape[:2]

        # Set the screen resolution (your screen: 1366x768)
        screen_width, screen_height = 1366, 768

        gaze_x, gaze_y, timestamp = [], [], []

        while time.time() - start_time >= 30:  # Ensures the loop runs for exactly 30 seconds
            _, frame = webcam.read()
            gaze.refresh(frame)
            new_frame = gaze.annotated_frame()

            # Resize the new_frame to match the img size (if needed)
            new_frame_resized = cv2.resize(new_frame, (img_width, img_height))
            horizontal_ratio = gaze.horizontal_ratio()
            vertical_ratio = gaze.vertical_ratio()

            # Add only if horizontal and vertical ratios are not NaN
            if not (pd.isna(horizontal_ratio) or pd.isna(vertical_ratio)):
                gaze_x.append(horizontal_ratio)
                gaze_y.append(vertical_ratio)
                timestamp.append(time.time() - start_time)

            alpha = 0.9

            if new_frame_resized is not None:
                # Overlay the resized new_frame on the img
                blended_frame = cv2.addWeighted(new_frame_resized, 1 - alpha, img, alpha, 0)

                # Print GAZE coordinates at the bottom center
                if gaze_x and gaze_y:
                    text = f"Gaze: (X={gaze_x[-1]}, Y={gaze_y[-1]})"
                else:
                    text = "Gaze: Searching coordinates..."

                # Calculate position to print text at the bottom center with a larger size
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 2.0, 3)[0]  # Increase font size to 2.0 and thickness to 3
                text_position = ((img_width - text_size[0]) // 2, img_height - 20)  # Adjust the position if needed
                cv2.putText(blended_frame, text, text_position, cv2.FONT_HERSHEY_DUPLEX, 2.0, (255, 0, 0), 3)  # Larger text size and thicker

                # Fullscreen display
                cv2.namedWindow("Gaze Detection", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Gaze Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow("Gaze Detection", blended_frame)
                cv2.waitKey(1)

        webcam.release()
        cv2.destroyAllWindows()

        if gaze_x:
            file_path = os.path.join(coordinates_folder, f"{user_id}_{name}.xlsx")
            os.makedirs(coordinates_folder, exist_ok=True)
            df = pd.DataFrame({
                "ID": [user_id] * len(timestamp),
                "Name": [name] * len(timestamp),
                "Age": [age] * len(timestamp),
                "Gender": [gender] * len(timestamp),
                "City": [city] * len(timestamp),
                "SEC's": [sec] * len(timestamp),
                "Brand": [brand] * len(timestamp),
                "Timestamp (s)": timestamp,
                "Gaze X": gaze_x,
                "Gaze Y": gaze_y
            })
            file_path = os.path.join(coordinates_folder, f"{user_id}_{name}.xlsx")  # Corrected line
            df.to_excel(file_path, index=False)
            gaze_data = df  # Store the data
            
# The user information dialog
class UserInformationDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("User Information")

        # Create labels and entry for ID, name, age, gender, city, sec and Brand
        self.id_label = tk.Label(self.top, text="ID:")
        self.id_label.pack()
        self.id_var = tk.StringVar()
        self.id_entry = tk.Entry(self.top, textvariable=self.id_var)
        self.id_entry.pack()

        self.name_label = tk.Label(self.top, text="Name:")
        self.name_label.pack()
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.top, textvariable=self.name_var)
        self.name_entry.pack()

        self.age_label = tk.Label(self.top, text="Age:")
        self.age_label.pack()
        self.age_var = tk.StringVar()
        self.age_dropdown = ttk.Combobox(self.top, textvariable=self.age_var, values=["09-12", "13-19", "20-30"])
        self.age_dropdown.pack()

        self.gender_label = tk.Label(self.top, text="Gender:")
        self.gender_label.pack()
        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(self.top, textvariable=self.gender_var, values=["Male", "Female"])
        self.gender_dropdown.pack()

        self.city_label = tk.Label(self.top, text="City:")
        self.city_label.pack()
        self.city_var = tk.StringVar()
        self.city_dropdown = ttk.Combobox(self.top, textvariable=self.city_var, values=["Karachi", "Lahore", "Multan", "Faisalabad"])
        self.city_dropdown.pack()

        self.SEC_label = tk.Label(self.top, text="SEC's")
        self.SEC_label.pack()
        self.sec_var = tk.StringVar()
        self.sec_dropdown = ttk.Combobox(self.top, textvariable=self.sec_var, values=["SEC-A", "SEC-B", "SEC-C", "SEC-D"])
        self.sec_dropdown.pack()

        self.brand_label = tk.Label(self.top, text="Brands")
        self.brand_label.pack()
        self.brand_var = tk.StringVar()
        self.brand_dropdown = ttk.Combobox(self.top, textvariable=self.brand_var, values=["Lemon Sandwich", "Chocolate Sandwich", "RIO Double Chocolate", "Prince", "Oreo"])
        self.brand_dropdown.pack()

        # Create a button to start detection
        self.start_button = tk.Button(self.top, text="Start Detection", command=self.start_detection)
        self.start_button.pack()

        # Variable to check if the dialog is cancelled
        self.cancelled = False

    def start_detection(self):
        user_id = self.id_var.get()
        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        city = self.city_var.get()
        sec = self.sec_var.get()
        brand = self.brand_var.get()

        if not user_id or not user_id.isdigit():
            tk.messagebox.showwarning("Warning", "Please enter a numeric ID.")
        elif not name:
            tk.messagebox.showwarning("Warning", "Please enter a name.")
        else:
            self.cancelled = False
            self.top.destroy()

    def get_user_info(self):
        user_id = self.id_var.get()
        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        city = self.city_var.get()
        sec = self.sec_var.get()
        brand = self.brand_var.get()
        return user_id, name, age, gender, city, sec, brand

# Create a Tkinter window
root = tk.Tk()
root.title("Gaze Detection")

# Function to close the program when the window is closed
root.protocol("WM_DELETE_WINDOW", on_close)

# Create a button to start gaze detection
start_detection_button = tk.Button(root, text="Start Detection", command=start_detection)
start_detection_button.pack()

# Main loop
root.mainloop()