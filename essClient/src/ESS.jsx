import { Routes, Route } from "react-router-dom";
import "./ESS.css";
import NavBar from './Navbar';
import { useState } from "react";
import  Auth  from "./Auth";
import Dashboard from "./Dashboard";
function ESS() {
  const [fileData, setFileData] = useState(null);
  if (fileData) {
    console.log(fileData);
  }
  return (
    <>
      {/* <NavBar/> */}
      <Routes>
        <Route
          path="/"
          element={<Dashboard/>}
        />
        <Route path="/Login" element={<Auth/>} />
        <Route path="/Dashboard" element={<Dashboard/>} /> 
       </Routes>
      </>
  );
}

export default ESS;
