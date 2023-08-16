import subprocess
import os
import signal

from flask import Flask, jsonify, request
from flask_cors import CORS

from call_emergency import call_emergency
from find_symptoms import symptoms_validation
from inference_pipeline import inference_pipeline

app = Flask(__name__)
CORS(app)

process = None


def start_subprocess():
    global process
    process = subprocess.Popen(['C:/Users/DELL/anaconda3/python.exe',
                                'C:/Users/DELL/OneDrive/Documents/Projects/BEFAST/Befast_Stroke_Detection_App/backend/mediapipe_display.py'])
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


@app.route('/call_emergency', methods=['GET'])
def call_emergency():
    call_emergency()
    return jsonify({'message': 'Calling emergency is success!'})


@app.route('/validate', methods=['GET'])
def get_validations():
    isSymptomsFound = symptoms_validation()

    response = {
        'message': 'Validate is success!',
        'isSymptomsFound': isSymptomsFound
    }

    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
