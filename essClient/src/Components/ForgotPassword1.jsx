import React from 'react';
// import Login  from './Login.jsx';

import Forgot_password from './Assests/Forgot_password.jpg';
import ForwardToInboxTwoToneIcon from '@mui/icons-material/ForwardToInboxTwoTone';
import { useNavigate } from 'react-router-dom';
const ForgetPassword=()=>{ 
  const navigate=useNavigate();
  return ( 
      <div className="container_Forgot">
       <img className="forgot_pass" src={Forgot_password} alt="" srcset="" />
        <div className="header">
          <div className="text">Forgot Your Password ? </div>
          <div className="underlineForgot"></div>
          <span className="instruction">Confirm Your email we will send the instruction</span>
          <div className="inputs">
            <div className="input">
             <ForwardToInboxTwoToneIcon className="forgot_icon"></ForwardToInboxTwoToneIcon>
             <input type="email" placeholder="Email"/>
            </div>
          </div>
          {/* <div className="forgetPassword">Forgot Password? <span>Click Here!</span></div> */}
          <div className="submit-container">
              <button className="ResetCode"><span onClick={()=>navigate("/ResetPassword")}> Send Code </span></button> 
          </div>
        </div>
      </div>
  )
}
export default ForgetPassword;
