import React from "react";
import "./NavbarCSS.css";
import BrandLogo from "./Brand_logo.svg";
// import { Grid } from "@mui/material";
// import FileInput from ".file-input";
// import FileConverter from "./file-converter";

export default function Navbar() {
  // const [pdfFile, setPdfFile] = useState(null);
  return (
    <>
      <nav>
        <div className="container-nav">
          <div className="logo1">
            <img className="logo" src={BrandLogo} alt="Brand logo" />
            <span className="logo_heading">ESS</span>
          </div>
          <a href="/" className="List">
            DashBoard
          </a>
          <a href="/SignUp" className="List">
            Sign Up
          </a>
          <a href="/Login" className="List">
            Sign In
          </a>
          <a href="/" className="List">
            Sign Out
          </a>
        </div>
      </nav>
      
    </>
  );
}
