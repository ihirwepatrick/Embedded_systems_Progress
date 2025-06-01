import os
import time
import shutil
import subprocess

# Define the paths
camera_folder = "./camera"  # Replace with the folder where the camera saves pictures
uploaded_folder = "./uploads"  # Replace with the folder to store uploaded pictures
upload_url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Ensure the uploaded folder exists
os.makedirs(uploaded_folder, exist_ok=True)

# Monitor the folder
print(f"Monitoring folder: {camera_folder}")
while True:
    try:
        # List all files in the camera folder
        files = [f for f in os.listdir(camera_folder) if os.path.isfile(os.path.join(camera_folder, f))]

        for file in files:
            file_path = os.path.join(camera_folder, file)

            # Wait for 30 seconds before uploading the file
            print(f"Waiting 30 seconds before uploading: {file}")
            time.sleep(30)

            # Use curl to upload the file
            try:
                response = subprocess.run(
                    ["curl", "-X", "POST", "-F", f"imageFile=@{file_path}", upload_url],
                    capture_output=True,
                    text=True,
                )

                if response.returncode == 0:
                    print(f"Successfully uploaded: {file}")

                    # Move the file to the uploaded folder
                    shutil.move(file_path, os.path.join(uploaded_folder, file))
                    print(f"Moved {file} to uploaded folder.")
                else:
                    print(f"Failed to upload {file}: {response.stderr}")
            except Exception as e:
                print(f"Error uploading {file}: {e}")

    except Exception as e:
        print(f"Error monitoring folder: {e}")

    # Wait a bit before checking the folder again
    time.sleep(5)
