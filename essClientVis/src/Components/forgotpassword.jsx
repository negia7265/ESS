import React from 'react';
import './LoginSignup.css'
// import Login  from './Login.jsx';


// import user_icon from './Assests/person.png';
import email_icon from './Assests/email.png';
// import password from './Assests/password.png';

const ForgetPassword=()=>{ 
  return ( 
      <div className="container_Forgot">
       <img className="forgot_pass" src={Forgot_Password} alt="" srcset="" />
        {/* <div className="header">
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
          {/* <div className="submit-container">
              <button className="ResetCode">Send Code </button> 
          </div>
        </div> */} 
      </div>
  )
}
export default ForgetPassword;
