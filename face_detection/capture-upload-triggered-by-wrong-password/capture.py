import os
import time
import shutil
import subprocess
import cv2

# Define the paths
captures_folder = "./captures"  # Folder to save captured pictures
uploaded_folder = "./uploads"  # Folder to store uploaded pictures

upload_url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Ensure the folders exist
os.makedirs(captures_folder, exist_ok=True)
os.makedirs(uploaded_folder, exist_ok=True)

#modify this variable and set to "wrong to test the password capturing feature when user makes an incorrect attempt"
pswd_status = "correct"
# Simulated function to monitor password status
def check_password_status(pswd_status):
    # Replace this logic with real monitoring for password status
    # Simulate an incorrect password attempt
    return pswd_status

# Function to capture a picture using the camera
def capture_image():
    cap = cv2.VideoCapture(0)  # Open the first camera
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return None

    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        return None

    # Generate a unique filename based on the current timestamp
    file_name = os.path.join(captures_folder, f"capture_{int(time.time())}.jpg")
    cv2.imwrite(file_name, frame)  # Save the captured image
    cap.release()
    return file_name

# Monitor password status and take action
print("Monitoring password attempts...")
while True:
    try:
        # Check password status
        password_status = check_password_status(pswd_status)
        if password_status == "wrong":
            print("Incorrect password detected. Capturing image...")
            captured_image = capture_image()

            if captured_image:
                print(f"Captured image saved: {captured_image}")

                # Wait for 30 seconds before uploading
                print(f"Waiting 30 seconds before uploading: {captured_image}")
                time.sleep(30)

                # Use curl to upload the captured image
                try:
                    response = subprocess.run(
                        ["curl", "-X", "POST", "-F", f"imageFile=@{captured_image}", upload_url],
                        capture_output=True,
                        text=True,
                    )

                    if response.returncode == 0:
                        print(f"Successfully uploaded: {captured_image}")

                        # Move the file to the uploaded folder
                        shutil.move(captured_image, os.path.join(uploaded_folder, os.path.basename(captured_image)))
                        print(f"Moved {captured_image} to uploaded folder.")
                    else:
                        print(f"Failed to upload {captured_image}: {response.stderr}")
                except Exception as e:
                    print(f"Error uploading {captured_image}: {e}")
        else:
            print("Password status OK.")

    except Exception as e:
        print(f"Error monitoring password status: {e}")

    # Wait a bit before rechecking the password status
    time.sleep(5)
