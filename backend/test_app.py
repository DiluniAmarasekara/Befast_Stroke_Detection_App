import requests

# Specify the URL of the Flask server
url = 'http://localhost:5000/get_video_prediction' 

# Open the video file as binary
file_path = "C://Users//DELL//Downloads//video_2.mpg"

with open(file_path, 'rb') as file:
    # Create a dictionary with the file data
    files = {'video': file}

    # Send a POST request to the server with the video file
    response = requests.post(url, files=files)

# Check the response from the server
if response.status_code == 200:
    data = response.json()  # Parse the JSON response
    prediction = data['prediction']  # Get the prediction value
    print('Video saved successfully.')
    print('Prediction:', prediction)  # Print the prediction
else:
    print('Error occurred while saving the video.')

import requests
import cv2

# Endpoint URLs
# start_url = 'http://localhost:5000/start_video'
# stop_url = 'http://localhost:5000/stop_video'

# # Start video capture
# response = requests.get(start_url)
# if response.status_code == 200:
#     print('Video capture started.')
# else:
#     print('Failed to start video capture.')

# import time 
# time.sleep(20)

# # # Stop video capture
# response = requests.get(stop_url)
# if response.status_code == 200:
#     print('Video capture stopped.')
# else:
#     print('Failed to stop video capture.')

