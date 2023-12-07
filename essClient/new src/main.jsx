import React from "react";
import ReactDOM from "react-dom/client";
import { Routes, Route } from "react-router-dom";
import "./ESS.css";
import Dashboard from "./Dashboard";
import NavBar from './Navbar';
import { BrowserRouter } from "react-router-dom";
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>     
    <NavBar/>
      <Routes>
        <Route path="/" element={<Dashboard/>}/>
       </Routes>
    </BrowserRouter>
  </React.StrictMode>
);