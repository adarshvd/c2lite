import cv2
import tkinter as tk
from PIL import Image, ImageTk

def show_frame():
    # Capture frame from video source
    ret, frame = cap.read()
    if ret:
        # Resize the frame while maintaining aspect ratio
        height, width, _ = frame.shape
        new_width = 640  # Adjust desired width
        new_height = int(new_width * height / width)
        frame = cv2.resize(frame, (new_width, new_height))

        # Convert to PIL Image for Tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk  # Keep a reference
        label.configure(image=imgtk)
    label.after(10, show_frame)  # Update every 10 ms

# Define window size
width = 640
height = 480

# Create Tkinter window
root = tk.Tk()
root.geometry(f"{width}x{height}")  # Set window size

# Create label to display video frames
label = tk.Label(root)
label.pack()

# Start video capture
cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.111:554/snl/live/1/1")

# Start the video display loop
show_frame()

# Handle window close event
root.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), cv2.destroyAllWindows(), root.destroy()))

root.mainloop()
