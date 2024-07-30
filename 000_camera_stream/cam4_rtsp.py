import cv2

# Define the desired window size
width = 640
height = 480

cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.111:554/snl/live/1/1")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame (optional)
    frame = cv2.resize(frame, (width, height))

    # Create the pop-up window and set its size
    cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera Feed", width, height)

    # Display the frame in the pop-up window
    cv2.imshow("Camera Feed", frame)

    # Check for any key press (including 'q' and the 'x' button on the window)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # 27 is the escape key code
        break

cap.release()
cv2.destroyAllWindows()
