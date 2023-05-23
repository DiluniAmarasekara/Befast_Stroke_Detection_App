import React, { useState, useRef } from 'react';
import axios from 'axios';
import './Lipsigns.css';
import Navbar from '../components/Navbar';

function Lipsigns() {
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [recording, setRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);

  const startRecording = () => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        mediaRecorderRef.current = new MediaRecorder(stream);
        mediaRecorderRef.current.addEventListener('dataavailable', handleDataAvailable);
        mediaRecorderRef.current.start();
        setRecording(true);
      })
      .catch((error) => {
        console.error('Error accessing webcam:', error);
      });
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  const handleDataAvailable = (event) => {
    if (event.data.size > 0) {
      setRecordedChunks((prevChunks) => prevChunks.concat(event.data));
    }
  };

  const handlePredict = () => {
    if (recordedChunks.length > 0) {
      const recordedBlob = new Blob(recordedChunks, { type: 'video/mp4' });
      const formData = new FormData();
      formData.append('video', recordedBlob, 'recordedVideo.mp4');

      axios.post('http://127.0.0.1:5000/get_prediction', formData)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.error('Error sending video to Flask API:', error);
        });
    }
  };

  return (
    <>
      <Navbar />
      <div className='lip_container'>
        <div className='l_row text_row'>
          <div className='l_left_h'>
            <h2 className='lip_h'>Lip Sync Identification</h2>
          </div>
          <div className='l_right_h'>
            <h2 className='lip_pred'>Prediction: x if x se ding</h2>
          </div>
        </div>
        <div className='l_row btn_row'>
          <button className='str_rec_btn' onClick={startRecording}>Start Recording</button>
          <button className='stp_rec_btn' onClick={stopRecording}>Stop Recording</button>
          <button className='pred_btn' onClick={handlePredict}>Predict</button>
          <button className='validate_btn' disabled={true}>Validate</button>
        </div>
        <div className='l_row video_row'>
          <video ref={videoRef} className='video_player' controls>
            {recordedChunks.length > 0 && (
              <source src={URL.createObjectURL(new Blob(recordedChunks, { type: 'video/mp4' }))} type='video/mp4' />
            )}
          </video>
        </div>
      </div>
    </>
  );
}

export default Lipsigns;