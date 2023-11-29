import React from 'react';
// import Login  from './Login.jsx';
0

// import user_icon from './Assests/person.png';
// import email_icon from './Assests/email.png';
// import password from './Assests/password.png';
import Reset_Pass from './Assests/Reset_pass.jpg';
import LockOpenTwoToneIcon from '@mui/icons-material/LockOpenTwoTone';
import LockClockTwoToneIcon from '@mui/icons-material/LockClockTwoTone';
import CheckCircleTwoToneIcon from '@mui/icons-material/CheckCircleTwoTone';
// import google from './Assests/google.jpeg';
// import facebook from './Assests/facebook.jpeg';
// import GoogleIcon from '@mui/icons-material/Google';
// import FacebookIcon from '@mui/icons-material/Facebook';
// import Button from '@mui/material/Button';
// const [page, setPage] = useState("");
const ResetPassword=()=>{ 
  return ( 
      <div className="container_Reset"> 
        <div className="header"> 
           <img  class="Reset_img" src={Reset_Pass} alt="Reset_pass" srcset="" />
          <div className="text">Reset Password </div>
          <div className="underlineForgot"></div>
          <span className="instruction">Set the New password for your account so that you can login and access all the features </span>
          <div className="inputs">
          <div className="input">
             {/* <img src={password} alt="" srcset="" /> */}
             <CheckCircleTwoToneIcon className='reset_icons'></CheckCircleTwoToneIcon>
             <input type="verificationcode" placeholder="Verification Code"/>
            </div>
            <div className="input">
             {/* <img src={password} alt="" srcset="" /> */}
             <LockOpenTwoToneIcon  className='reset_icons'></LockOpenTwoToneIcon>
             <input type="password" placeholder="New Password"/>
            </div>
            <div className="input">
             {/* <img src={password} alt="" srcset="" /> */}
             <LockClockTwoToneIcon  className='reset_icons'></LockClockTwoToneIcon>
             <input type="password" placeholder="Confirm Password"/>
            </div>
          </div>
          <div className="submit-container">
              <button className="Reset">Reset</button> 
          </div>
        </div>
      </div>
  )
}
export default ResetPassword;
