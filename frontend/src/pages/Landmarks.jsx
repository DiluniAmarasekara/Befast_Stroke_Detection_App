import React from 'react'
import './Landmarks.css'
import Navbar from '../components/Navbar';
import { AiOutlinePlayCircle } from "react-icons/ai";
import { FiStopCircle } from "react-icons/fi";
import { MdOutlineNextPlan } from "react-icons/md"
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios';

function Landmarks() {
  const navigate = useNavigate();

  const handleStartClick = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/start_video');
      console.log(response);
    } catch (error){
      console.error(error)
    }
  };

  const handleStopClick = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/stop_video');
      console.log(response);
      if (response.data.message === 'Video capture stopped') {
        navigate('/lipsign');
      } else{
        console.log('[ERROR] Respose not recieved')
      }
    } catch (error){
      console.error(error)
    }
  };
  return (
    <div>
      <Navbar/>
      <div className='landmark_container'>
        <div className='left_lcontainer'>
          <h2 className='landmark_h'>Fast and effective stroke detection mechanism</h2>
          <p className="landmark_p">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut tempus est id mauris lacinia,<br/>a malesuada neque lacinia. Sed luctus facilisis hendrerit. </p>
        </div>
        <div className='right_lcontainer'></div>
        <div className='overlay_container'>
          <h2 className='overlay_h'>Key Landmark Detection</h2>
          <div className='overlay_btn_container'>
            <button className='overlay_btn obtn1' onClick={handleStartClick}>
              <AiOutlinePlayCircle className='overlay_icon play_i'/>
              <span className='overlay_label'>Start</span>
            </button>
            <button className='overlay_btn obtn2' onClick={handleStopClick}>
              <FiStopCircle className='overlay_icon stop_i'/>
              <span className='overlay_label'>Stop</span>
            </button>
            <Link to="/lipsign" className="linkStyle">
              <button className='overlay_btn obtn3'>
                <MdOutlineNextPlan className='overlay_icon next_i'/>
                <span className='overlay_label next_label'>Next</span>
              </button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Landmarks