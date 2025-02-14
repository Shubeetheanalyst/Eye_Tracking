import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import cv2
import time
import pandas as pd
import numpy as np

def open_camera_with_gridlines():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    cv2.namedWindow("Adjust Face", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Adjust Face", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video")
            break

        frame = cv2.flip(frame, 1)

        # Draw gridlines (3x3)
        grid_color = (0, 255, 0)  
        thickness = 1

        for i in range(1, 3):  
            y = i * frame.shape[0] // 3
            x = i * frame.shape[1] // 3
            cv2.line(frame, (0, y), (frame.shape[1], y), grid_color, thickness)
            cv2.line(frame, (x, 0), (x, frame.shape[0]), grid_color, thickness)

        cv2.putText(frame, "Adjust your face and press 'M' to start.", (20, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow("Adjust Face", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('m'):
            print("Starting detection process...")
            break
        if key == 27:
            print("Exiting camera view...")
            cap.release()
            cv2.destroyAllWindows()
            return

    cap.release()
    cv2.destroyAllWindows()
    start_detection()

def start_detection():
    user_id = variables["ID"].get()
    name = variables["Name"].get()
    age = variables["Age"].get()
    gender = variables["Gender"].get()
    city = variables["City"].get()
    sec = variables["SEC"].get()
    brand = variables["Brand"].get()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    cv2.namedWindow("Eye Detection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Eye Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    brand_image_path = f"images/{brand}.jpg"
    if os.path.exists(brand_image_path):
        brand_image = cv2.imread(brand_image_path)
        brand_image = cv2.resize(brand_image, (1920, 700))
        background = np.zeros((1080, 1920, 3), dtype=np.uint8)
        y_offset = (1080 - 700) // 2  # Ensure picture is centered
        background[y_offset:y_offset + 700, 0:1920] = brand_image
    else:
        print("Image not found, skipping overlay.")
        background = np.zeros((1080, 1920, 3), dtype=np.uint8)

    start_time = time.time()
    while time.time() - start_time < 3:
        ret, _ = cap.read()
        if not ret:
            break
        cv2.imshow("Eye Detection", background)

    eye_cascade_path = os.path.join(os.path.dirname(__file__), "haarcascade_eye.xml")
    eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
    eye_x, eye_y, timestamp = [], [], []
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (1920, 1080))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.2, 2, minSize=(50, 50))

        blended_frame = cv2.addWeighted(frame, 0.01, background, 0.9, 0)

        if len(eyes) == 0:
            cv2.putText(blended_frame, "Face Not Detected", (100, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            for (x, y, w, h) in eyes:
                eye_center_x = x + w // 2
                eye_center_y = y + h // 2

                # Ensure eyes are inside the brand image
                if y_offset <= eye_center_y <= y_offset + 700:
                    cv2.rectangle(blended_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    eye_x.append(eye_center_x)
                    eye_y.append(eye_center_y - y_offset)  # Offset adjustment
                    timestamp.append(time.time() - start_time)

        cv2.imshow("Eye Detection", blended_frame)
        if cv2.waitKey(1) & 0xFF == 27 or time.time() - start_time >= 20:
            break

    cap.release()
    cv2.destroyAllWindows()

    df = pd.DataFrame({
        "ID": [user_id] * len(timestamp),
        "Name": [name] * len(timestamp),
        "Age": [age] * len(timestamp),
        "Gender": [gender] * len(timestamp),
        "City": [city] * len(timestamp),
        "SEC": [sec] * len(timestamp),
        "Brand": [brand] * len(timestamp),
        "Timestamp (s)": timestamp,
        "Eye X": eye_x,
        "Eye Y": eye_y
    })

    coordinates_folder = "COORDINATES"
    os.makedirs(coordinates_folder, exist_ok=True)
    df.to_excel(os.path.join(coordinates_folder, f"{user_id}_{name}.xlsx"), index=False)

    for field in variables:
        variables[field].set("")

    print("Process Complete!")

# Initialize the Tkinter window
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Eye Tracking App")
root.geometry("280x400")  # Adjusted size
root.configure(bg="#1e1e1e")  # Dark theme

# Define font styles
label_font = ("Helvetica", 10, "bold")
entry_font = ("Helvetica", 10)

# Create the form frame with padding
frame = ctk.CTkFrame(root, fg_color="#1e1e1e")
frame.pack(expand=True, fill="both", padx=10, pady=10)

# Title label
app_title = ctk.CTkLabel(frame, text="Eye Tracking App", font=("Helvetica", 14, "bold"))
app_title.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

# Create form fields
fields = ["ID", "Name", "Age", "Gender", "City", "SEC", "Brand"]
variables = {}
values = {
    "Age": ["20-24", "25-30", "31-35"],
    "Gender": ["Male", "Female"],
    "City": ["Karachi", "Lahore", "Rawalpindi", "Quetta", "Mardan", "Peshawar"],
    "SEC": ["SEC-A", "SEC-B", "SEC-C", "SEC-D"],
    "Brand": ["MNP-C", "MNP-EP", "MNP-LC", "MNP-MC"]
}

for i, field in enumerate(fields, start=1):
    label = ctk.CTkLabel(frame, text=f"{field}:", font=label_font)
    label.grid(row=i, column=0, sticky="w", pady=5, padx=5)
    
    if field in values:
        var = tk.StringVar(value=f"Select {field}")
        entry = ctk.CTkComboBox(frame, variable=var, values=values[field], font=entry_font, width=200)
    else:
        var = tk.StringVar()
        entry = ctk.CTkEntry(frame, textvariable=var, font=entry_font, width=200)
    
    entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
    variables[field] = var

# Start Detection Button
start_button = ctk.CTkButton(
    frame, 
    text="Start Detection", 
    font=("Helvetica", 12, "bold"), 
    height=35, 
    command=open_camera_with_gridlines  # Call the function
)
start_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=15, padx=5, sticky="nsew")

# Run the UI
root.mainloop()