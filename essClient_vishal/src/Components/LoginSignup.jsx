import React from 'react'
import './LoginSignup.css'

import user_icon from './Assests/person.png';
import email_icon from './Assests/email.png';
import password from './Assests/password.png';
import google from './Assests/google.jpeg';
import facebook from './Assests/facebook.jpeg';
const LoginSignUp=()=>{
  return (
      <div className="containerd">
        <div className="header">
          <div className="text">SignUp</div>
          <div className="underline"></div>
          <div className="inputs">
            <div className="input">
             <img src={user_icon} alt="" srcset="" />
             <input type="text" placeholder="Name"/>
            </div>
            <div className="input">
             <img src={email_icon} alt="" srcset="" />
             <input type="email" placeholder="Email"/>
            </div>
                        <div className="input">
             <img src={password} alt="" srcset="" />
             <input type="password" placeholder="Password"/>
            </div>
          </div>
          <div className="forgetPassword">Forgot Password? <span>Click Here!</span></div>
          <div className="submit-container">
              <button className="Signup">SignUp</button> 
              <hr className="or"></hr>
              <div className="loginBox"> 
              <div className="Login">
              <img src={google} alt="" srcset="" />
              <span  class="text1">Login With Google</span> 
              </div> 
              <div className="Login">
              <img src={facebook} alt="" srcset="" />
              <span  class="text1">Login With Facebook</span> 
              </div> 
              </div>
          </div>
        </div>
      </div>
  )
}
export default LoginSignUp;
