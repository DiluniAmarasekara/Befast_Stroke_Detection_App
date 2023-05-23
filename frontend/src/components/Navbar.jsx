import React from 'react'
import './Navbar.css';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <div className='navbar'>
      <img src={require('../assests/logo2.png')} alt="Logo" className="navbar_logo" />
      <span className='nav_span'>Befast Stroke Detector</span>
    </div>
  )
}

export default Navbar