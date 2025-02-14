# Eye Tracking Application

This is a **Tkinter-based Eye Tracking Application** that captures user eye movement and records it in an Excel file. The application includes a **camera interface with gridlines**, eye detection using **OpenCV**, and saves tracking data for further analysis.

## **Features**
- **Tkinter GUI** for user input
- **OpenCV-based eye tracking**
- **Overlay brand images** for focused eye-tracking
- **Saves data** (User details + Eye coordinates) to an Excel file
- **Dark theme UI using CustomTkinter**

---

## **Requirements**
Make sure you have **Python 3.7+** installed. The following libraries are required:

```sh
pip install opencv-python pandas numpy pillow customtkinter openpyxl
```

---

## **How to Run the Application**

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/eye-tracking-app.git
   cd eye-tracking-app
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Ensure Haarcascade file is present:**
   - Download `haarcascade_eye.xml` from OpenCV repository ([Link](https://github.com/opencv/opencv/tree/master/data/haarcascades)).
   - Place it in the same directory as the script.

4. **Run the application:**
   ```sh
   app.py
   ```

---

## **Usage Instructions**

1. **Enter user details** (ID, Name, Age, Gender, City, SEC, Brand) in the GUI.
2. **Click on "Start Detection".**
3. **Adjust your face** within the grid and press `M` to start.
4. **Eye tracking starts** (Runs for ~20 seconds).
5. **Captured data is saved** in the `COORDINATES/` folder as an Excel file.
6. **Press `ESC` to exit.**

---

## **Building an Executable (Optional)**
To create a **Windows EXE** file using **PyInstaller**, run:

```sh
pyinstaller --onefile --add-data "haarcascade_eye.xml;." app.py
```
This will generate an `app.exe` inside the `dist/` folder.

---

## **Folder Structure**
```
/eye-tracking-app
│── images/               # Store brand images here
│── COORDINATES/          # Generated Excel files
│── haarcascade_eye.xml   # Required for eye detection
│── app.py                # Main script
│── README.md             # Project documentation
│── requirements.txt       # Dependencies
```

---

## **Troubleshooting**

1. **Camera not opening?**
   - Check if another application is using the camera.
   - Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`.

2. **Haarcascade file error?**
   - Ensure `haarcascade_eye.xml` is in the project folder.
   - Use the correct path in the code:
     ```python
     eye_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), "haarcascade_eye.xml"))
     ```

3. **No eyes detected?**
   - Ensure proper lighting conditions.
   - Adjust face position within the grid.
