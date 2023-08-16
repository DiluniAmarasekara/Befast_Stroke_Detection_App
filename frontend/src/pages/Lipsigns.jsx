import React, {useState, useRef, useEffect} from 'react';
import axios from 'axios';
import {RecordWebcam, useRecordWebcam} from "react-record-webcam";
import './Lipsigns.css';
import Navbar from '../components/Navbar';
import {MdOutlineReplayCircleFilled, MdDownloadForOffline} from "react-icons/md";
import {Link} from "react-router-dom";

const OPTIONS = {
    fileName: "video", mimeType: "video/mpg", width: 500, height: 200, disableLogs: true
};

function Lipsigns() {
    const recordWebcam = useRecordWebcam(OPTIONS);
    const videoRef = useRef(null);
    const downloadButtonRef = useRef(null);
    const [prediction, setPrediction] = useState('Prediction here')

    const getBlob = async (blob) => {
        console.log(blob);
    };

    useEffect(() => {
        if (videoRef.current) {
            videoRef.current.srcObject = recordWebcam.webcamRef.current.srcObject;
        }
    }, [recordWebcam.webcamRef]);

    const sendRequestToApi = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/get_video_prediction');
            console.log(response);
            setPrediction(response.data.prediction);
        } catch (error) {
            console.log(error);
        }
    };

    const handleDownloadComplete = () => {
        setTimeout(() => {
            console.log('File download completed.');
            sendRequestToApi();
        }, 5000);
    };

    const handleDownloadError = () => {
        console.log('File download failed.');
    };

    const handlePredictButtonClick = async (blob) => {
        getBlob(blob);

        if (downloadButtonRef.current) {
            const downloadLink = downloadButtonRef.current;
            downloadButtonRef.current.addEventListener('click', handleDownloadComplete);
            downloadButtonRef.current.addEventListener('error', handleDownloadError);
            downloadButtonRef.current.click();
        }
    };

    return (<>
        <Navbar/>
        <div className='lip_container'>
            <div className='l_row text_row'>
                <div className='l_left_h'>
                    <h2 className='lip_h'>Lip Sync Identification</h2>
                </div>
                <div className='l_right_h'>
                    <h2 className='lip_pred'>Prediction: {prediction}</h2>
                </div>
            </div>
            <div className='l_row btn_row'>
                <RecordWebcam
                    options={OPTIONS}
                    render={(renderProps) => (<div>
                        <p>Camera Status: {renderProps.status}</p>
                        <div>
                            <button
                                disabled={renderProps.status === "OPEN" || renderProps.status === "RECORDING" || renderProps.status === "PREVIEW"}
                                onClick={renderProps.openCamera}
                                className='open_btn'>
                                Open Camera
                            </button>
                            <button
                                disabled={renderProps.status === "CLOSED"}
                                onClick={renderProps.closeCamera}
                                className='close_btn'>
                                Close Camera
                            </button>
                            <button
                                disabled={renderProps.status === "CLOSED" || renderProps.status === "RECORDING" || renderProps.status === "PREVIEW"}
                                onClick={renderProps.start}
                                className='str_rec_btn'>
                                Start Recording
                            </button>
                            <button
                                disabled={renderProps.status !== "RECORDING"}
                                onClick={renderProps.stop}
                                className='stp_rec_btn'>Stop Recording
                            </button>
                            <button
                                disabled={renderProps.status !== "PREVIEW"}
                                onClick={renderProps.retake}
                                className='retake_btn'>
                                <MdOutlineReplayCircleFilled className='lip_icon'/>
                            </button>
                            <button
                                ref={downloadButtonRef}
                                disabled={renderProps.status !== "PREVIEW"}
                                onClick={renderProps.download}
                                className='download_btn'>
                                <MdDownloadForOffline className='lip_icon'/>
                            </button>
                            <button
                                disabled={renderProps.status !== "PREVIEW"}
                                className='pred_btn'
                                onClick={async () => {
                                    const blob = await renderProps.getRecording();
                                    handlePredictButtonClick(blob);
                                }}
                            >Predict
                            </button>

                            <button className='validate_btn' disabled={renderProps.status !== "PREVIEW"}>
                                <Link to="/validates" className="linkStyle">Next Validate</Link>
                          </button>

                        </div>
                    </div>)
                    }
                />
            </div>
        </div>
    </>);
}

export default Lipsigns;