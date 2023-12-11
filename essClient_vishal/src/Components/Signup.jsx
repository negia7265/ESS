import React from 'react';
import './LoginSignup.css'
import { useNavigate } from 'react-router-dom';
// import Login  from './Login.jsx';


// import user_icon from './Assests/person.png';
import PersonOutlineTwoToneIcon from '@mui/icons-material/PersonOutlineTwoTone';
import EmailTwoToneIcon from '@mui/icons-material/EmailTwoTone';
import LockTwoToneIcon from '@mui/icons-material/LockTwoTone';
// import google from './Assests/google.jpeg';
// import facebook from './Assests/facebook.jpeg';
// import GoogleIcon from '@mui/icons-material/Google';
// import FacebookIcon from '@mui/icons-material/Facebook';
// import Button from '@mui/material/Button';
// const [page, setPage] = useState("");
const LoginSignUp=()=>{ 
  const navigate=useNavigate();
  return ( 
      <div className="containerd">
        <div className="header">
          <div className="text">SignUp</div>
          <div className="underline"></div>
          <div className="inputs">
            <div className="input">
             {/* <img src={user_icon} alt="" srcset="" /> */}
             <PersonOutlineTwoToneIcon className="person_icon"></PersonOutlineTwoToneIcon>
             <input type="text" placeholder="Name"/>
            </div>
            <div className="input">
             {/* <img src={email_icon} alt="" srcset="" /> */}
             <EmailTwoToneIcon className="person_icon"></EmailTwoToneIcon>
             <input type="email" placeholder="Email"/>
            </div>
              <div className="input">
             {/* <img src={password} alt="" srcset="" /> */}
            <LockTwoToneIcon className="person_icon"></LockTwoToneIcon>
             <input type="password" placeholder="Password"/>
            </div>
          </div>
          {/* <div className="forgetPassword">Forgot Password? <span>Click Here!</span></div> */}
          <div className="submit-container">
              <button className="Signup">SignUp</button> 
               {/* <hr className="or"></hr>  */}
              <div className="SignUpBox">  
              <span class="Acc">Already have an account ?</span> 
              <button class="LoginBtn"onClick={()=>navigate("/Login")}>Login Here</button>
              {/* <div className="Login"> */}
              {/* <img src={google} alt="" srcset="" /> */}
              {/* <GoogleIcon/> */}
              {/* <span  class="text1">Login With Google</span>  */}
              {/* </div>  */}
              {/* <div className="Login">
              <FacebookIcon/>
              {/* <img src={facebook} alt="" srcset="" /> */}
              {/* <span  class="text1">Login With Facebook</span>  */}
              {/* </div>  */}
              </div>
          </div>
        </div>
      </div>
  )
}
export default LoginSignUp;