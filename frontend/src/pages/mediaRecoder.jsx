import React, { useState } from 'react';
import './Lipsigns.css'
import Navbar from '../components/Navbar';
import { useReactMediaRecorder } from 'react-media-recorder';
import axios from 'axios';

function Lipsigns() {

  const [recordedVideo, setRecordedVideo] = useState(null);
  const { status, startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder({
    video: true,
    onStopBlob: (blobUrl, blob) => {
      setRecordedVideo(blob);
    },
  });

  const handlePredict = () => {
    if (recordedVideo) {
      const formData = new FormData();
      formData.append('video', recordedVideo);
      fetch('http://127.0.0.1:5000/get_video_prediction', {
        method: 'POST',
        body: formData
      })
        .then((response) => {
          // Handle the response from the Flask API
          return response.json();
        })
        .then((data) => {
          // Access the data returned by the Flask API
          console.log(data);
        })
        .catch((error) => {
          // Handle errors
          console.error(error);
        });
    }
  };  

  return (
    <>
      <Navbar/>
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
          <button className='validate_btn' disabled={true} >Validate</button>
        </div>
        <div className='video_player'>
          {mediaBlobUrl && (
            <video src={mediaBlobUrl} controls autoPlay loop className='recorded_video' />
          )}
        </div>
      </div>
    </>
  )
}

export default Lipsigns