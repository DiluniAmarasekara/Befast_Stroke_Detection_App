import subprocess
import os
import signal

from flask import Flask, jsonify, request
from flask_cors import CORS
from inference_pipeline import inference_pipeline

app = Flask(__name__)
CORS(app)

process = None

def start_subprocess():
    global process
    process = subprocess.Popen(['C:/Users/DELL/anaconda3/python.exe', 'C:/Users/DELL/OneDrive/Documents/Projects/BEFAST/Befast_Stroke_Detection_App/backend/mediapipe_display.py'])
    subprocess_pid = process.pid  # Get the subprocess PID
    return subprocess_pid

def stop_subprocess():
    global process
    if process is not None:
        process.terminate()

@app.route('/start_video', methods=['GET'])
def start_capture():
    start_subprocess()
    return jsonify({'message': 'Video capture started'})

@app.route('/stop_video', methods=['GET'])
def stop_capture():
    stop_subprocess()
    return jsonify({'message': 'Video capture stopped'})

@app.route('/get_video_prediction', methods=['POST'])
def get_video_prediction():
    # Get the video blob data from the request
    # video_blob = request.files['video']

    # print(video_blob)

    # # Save the blob data to a file locally
    # video_blob.save(file_path)
    # video_blob.save(file_path2)
    file_path = "C://Users//DELL//Downloads//video.mpg"
    
    # Run the inference pipeline
    prediction = inference_pipeline(file_path)

    os.remove(file_path)
    
    # Prepare the JSON response
    response = {
        'message': 'Prediction Successful',
        'prediction': prediction
    }

    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run()
