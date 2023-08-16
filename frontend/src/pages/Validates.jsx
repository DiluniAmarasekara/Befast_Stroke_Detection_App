import React, {useEffect, useState} from 'react';
import './Validates.css';
import Navbar from '../components/Navbar';
import {AiOutlinePhone, AiOutlineWarning} from "react-icons/ai";
import {MdOutlineNextPlan} from "react-icons/md";
import {Link, useNavigate} from 'react-router-dom';
import axios from 'axios';

function Validates() {
    const navigate = useNavigate();
    const [symptomsText, setSymptomsText] = useState('We are ready to validate your profile');
    const [isSymptomsFound, setIsSymptomsFound] = useState(false);

    useEffect(() => {
        // Call validation API on page initialization
        sendValidateToApi();
    }, []);

    const sendValidateToApi = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/validate');
            console.log(response);
            setIsSymptomsFound(response.data.isSymptomsFound);
            setSymptomsText(response.data.isSymptomsFound
                ? "We found BEFAST symptoms. Calling your emergency contact..."
                : "No BEFAST symptoms found.");
        } catch (error) {
            console.error(error)
        }
    };

    const handleCallClick = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/call_emergency');
            console.log(response);
            if (response.data.message === 'Calling emergency is success!') {
                navigate('/call');
            } else {
                console.log('[ERROR] Response not received');
            }
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <Navbar/>
            <div className='landmark_container'>
                <div className='right_lcontainer'></div>
                <div className='box_container'>
                    <h2 className='overlay_h'>{symptomsText}</h2>
                    <div className='overlay_btn_container'>
                        {isSymptomsFound ? (
                            <>
                                <button className='overlay_btn obtn2' onClick={handleCallClick}>
                                    <AiOutlinePhone className='overlay_icon stop_i'/>
                                    <span className='overlay_label'>Call emergency contact</span>
                                </button>
                                <Link to="/lipsign" className="linkStyle">
                                    <button className='overlay_btn obtn3'>
                                        <MdOutlineNextPlan className='overlay_icon next_i'/>
                                        <span className='overlay_label next_label'>Next Speech Check</span>
                                    </button>
                                </Link>
                            </>
                        ) : (
                            <p>No symptoms found.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Validates;
