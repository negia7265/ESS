import React from "react";
import "./Dashboard.css";
import BrandLogo from "./BrandLogo.svg";
import { useState } from "react";
// import {PDFtoIMG} from 'react-pdf-to-image';
// import file from './pdf-sample.pdf';

export default function Dashboard() {
  const [style, setStyle] = useState({ display: "none" }); //  have to fix issue
  const [pdfFile, setPdfFile] = useState(null);
  const [viwepdf, setViewPdf] = useState(null);
  const fileType = ["applicationpdf"];
  const handleChange = (e) => {
    let selectedfile = e.target.files[0];
    if (selectedfile) {
      if (selectedfile && fileType.includes(selectedfile.type)) {
        let reader = new FileReader();
        reader.readAsDataURL(selectedfile);
        reader.onload = (e) => {
          setPdfFile(e.target.result);
        };
      } else {
        setPdfFile(null);
      }
    } else {
      console.log("Please Select File");
    }
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    if (pdfFile !== null) { 
      console.lo
      setViewPdf(pdfFile);
    } else {
      setViewPdf(null);
    }
  };
  return (
    <>
      
      <div className="appinvoice">
        <div className="data_fetch">
          <div className="uploading">
            <div class="container-upload">
              <input type="file" onChange={handleChange} />
            </div>
            <button className="preview" onChange={handleSubmit}>
              Submit
            </button>
          </div>
          <div className="amount">
            <div className="head1">
              <span className="heading"> Date </span>
            </div>
            <span className="value">
              15- August- 2002
              <div className="confirm">
                {/* onMouseEnter=
                {(e) => {
                  setStyle({ display: "block" });
                }}
                onMouseLeave=
                {(e) => {        // Confirm Part 
                  setStyle({ display: "none" });
                }} */}
                <button style={style}>confirm</button>
              </div>
            </span>
            <span className="value">15- August- 2002</span>
            <span className="value">15- August- 2002</span>
            <span className="value">15- August- 2002</span>
            <button className="head">Enter Manually</button>
          </div>
          <div className="amount">
            <div className="head1">
              <span className="heading2">Distance Travelled</span>
            </div>
            <span className="value">90 km</span>
            <span className="value">90 km</span>
            <span className="value">90 km</span>
            <span className="value">90 km</span>
            <button className="head">Enter Manually</button>
          </div>
          <div className="amount">
            <div className="head1">
              <span className="heading3">Pickup Address </span>
            </div>
            <span className="value">10 ABC-Delhi Road</span>
            <span className="value">10 ABC-Delhi Road</span>
            <span className="value">10 ABC-Delhi Road</span>
            <span className="value">10 ABC-Delhi Road</span>
            <button className="head">Enter Manually</button>
          </div>
          <div className="amount">
            <div className="head1">
              <span className="heading2">Destination Address </span>
            </div>
            <span className="value">10 ABC-Delhi Road</span>
            <span className="value">10 ABC-Delhi Road</span>
            <span className="value">10 ABC-Delhi Road</span>
            <span className="value">10 ABC-Delhi Road</span>
            <button className="head">Enter Manually</button>
          </div>
        </div>
        <div className="pdf_preview">
          <div className="pdf_container">
          </div>
        </div>
      </div>
    </>
  );
}
