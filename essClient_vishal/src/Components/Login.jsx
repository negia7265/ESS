import React from 'react'
// import './LoginSignup.css'
import { useNavigate } from 'react-router-dom';

// import user_icon from './Assests/person.png';
// import email_icon from './Assests/email.png';
import PersonOutlineTwoToneIcon from '@mui/icons-material/PersonOutlineTwoTone';
import LockTwoToneIcon from '@mui/icons-material/LockTwoTone';
// import password from './Assests/password.png';
// import google from './Assests/google.jpeg';
// import facebook from './Assests/facebook.jpeg';
// import login from './Assests/Login.png';
import GoogleIcon from '@mui/icons-material/Google';
import FacebookIcon from '@mui/icons-material/Facebook';
const Login = () => {
  const navigate=useNavigate();
  return (
    <div className="containerd">
      <div className="header">
        {/* <img className="login_img" src={login} alt="" srcset="" /> */}
        <div className="text">Login</div>
        <div className="underline"></div>
        <div className="inputs">
          {/* <div className="input">
             <img src={user_icon} alt="" srcset="" />
             <input type="text" placeholder="Name"/>
            </div> */}
          <div className="input">
            {/* <img src={email_icon} alt="" srcset="" /> */}
            <PersonOutlineTwoToneIcon className="person_icon"></PersonOutlineTwoToneIcon>
            <input type="text" placeholder="Username" />
          </div>
          <div className="input">
            {/* <img src={password} alt="" srcset="" /> */}
            <LockTwoToneIcon className="person_icon"></LockTwoToneIcon>
            <input type="password" placeholder="Password" />
          </div>
        </div>
        <div className="forgetPassword_forgot">Forgot Password? <span onClick={()=>navigate("/Forgotpassword")}>Click Here!</span></div>
        {/* <div className="forgetPassword">Forgot Password? <span onClick={()=>navigate("/Forgotpassword")}>Click Here!</span></div> */}
        <div className="submit-container">
          <button className="MainLogin">Login</button>
          {/* <hr className="or"></hr> */}
          <div className="loginBox">
            <div className="Login">
            <GoogleIcon className="googleIcon"/>
              {/* <img src={GoogleIcon} alt="" srcset="" />
               */}
              <span class="text1">Login With Google</span>
            </div>
            <div className="Login">
              {/* <img src={FacebookIcon} alt="" srcset="" /> */}
              <FacebookIcon  className="googleIcon"></FacebookIcon>
              <span class="text1">Login With Facebook</span>
            </div>
          </div>
             </div>
        </div>
    </div>
  )
}
export default Login;