import React, {useState, useRef} from 'react';
import axios from 'axios';
import './Lipsigns.css';
import Navbar from '../components/Navbar';

function Lipsigns() {
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [recordedBlobs, setRecordedBlobs] = useState([]);
    const videoRef = useRef(null);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({video: true});
        const recorder = new MediaRecorder(stream);
        recorder.ondataavailable = handleDataAvailable;
        recorder.start();
        setMediaRecorder(recorder);
    };

    const stopRecording = () => {
        if (mediaRecorder) {
            mediaRecorder.stop();
        }
    };

    const handleDataAvailable = (event) => {
        if (event.data && event.data.size > 0) {
            setRecordedBlobs((prevBlobs) => [...prevBlobs, event.data]);
        }
    };

    const handleVideoPlay = () => {
        const videoPlayer = videoRef.current;
        const superBuffer = new Blob(recordedBlobs, {type: 'video/webm'});
        videoPlayer.src = window.URL.createObjectURL(superBuffer);
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
                    <button className='str_rec_btn' onClick={startRecording}>
                        Start Recording
                    </button>
                    <button className='stp_rec_btn' onClick={stopRecording}>
                        Stop Recording
                    </button>
                    <button className='pred_btn'>Predict</button>
                    <button className='validate_btn' disabled={true}>
                        Validate
                    </button>
                </div>
                <div className='l_row video_row'>
                    <video className='video_player' controls ref={videoRef} onPlay={handleVideoPlay}/>
                </div>
            </div>
        </>
    );
}

export default Lipsigns;


<button className='str_rec_btn'>Start Recording</button>
<button className='stp_rec_btn'>Stop Recording</button>
<button className='pred_btn'>Predict</button>
<button className='validate_btn' disabled={true}>Validate</button>
