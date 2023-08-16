import subprocess
import os
import signal

from flask import Flask, jsonify, request
from flask_cors import CORS

from call_emergency import call_emergency
from inference_pipeline import inference_pipeline
from mediapipe_display import perform_body_language_detection, stop_body_language_detection

app = Flask(__name__)
CORS(app)

process = None

is_symptoms_found = False


@app.route('/start_video', methods=['GET'])
def start_capture():
    # start_subprocess()
    global is_symptoms_found
    is_symptoms_found = False
    is_symptoms_found = perform_body_language_detection()
    return jsonify({'message': 'Video capture started'})


@app.route('/stop_video', methods=['GET'])
def stop_capture():
    stop_body_language_detection()
    return jsonify({'message': 'Video capture stopped'})


@app.route('/get_video_prediction', methods=['POST'])
def get_video_prediction():
    # Get the video blob data from the request
    file_path = "C://Users//DELL//Downloads//video.mpg"

    # Run the inference pipeline
    prediction = inference_pipeline(file_path)

    global is_symptoms_found

    if prediction != 'Today is beautiful!':
        is_symptoms_found = True

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
    global is_symptoms_found

    response = {
        'message': 'Validate is success!',
        'isSymptomsFound': is_symptoms_found
    }

    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
