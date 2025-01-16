import cv2
import requests
import time

# Server URL (replace with your actual server endpoint)
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load pre-trained Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

print("Starting face detection. Press 'q' to exit.")

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop the detected face
        face = frame[y:y + h, x:x + w]

        # Save the face image temporarily
        filename = f"detected_face_{int(time.time())}.jpg"
        cv2.imwrite(filename, face)

        # Upload the face image to the server
        with open(filename, "rb") as file:
            files = {"file": file}
            try:
                response = requests.post(UPLOAD_URL, files=files)
                if response.status_code == 200:
                    print(f"Uploaded {filename} successfully!")
                else:
                    print(f"Failed to upload {filename}. Server responded with status code {response.status_code}.")
            except Exception as e:
                print(f"Error uploading {filename}: {e}")

    # Show the webcam feed with rectangles around detected faces
    cv2.imshow("Face Detection", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
