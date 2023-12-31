import React from "react";
import ReactDOM from "react-dom/client";
import { Routes, Route } from "react-router-dom";
import "./ESS.css";
import Dashboard from "./Dashboard";
import NavBar from "./Navbar";
import { BrowserRouter } from "react-router-dom";
import styled from "styled-components";

const Ticket = styled.div`
  width: 100%;
  height: 300px;
  background-color: #3066b1;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 40px;
  font-weight: bold;
  color: #292929;

  &::before,
  &::after {
    position: absolute;
    content: "";
    width: 100%;
    height: 32px;
    background-repeat: repeat-x;
    background-size: 32px;
  }

  &::before {
    background: linear-gradient(-135deg, white 16px, transparent 0),
      linear-gradient(135deg, white 16px, transparent 0);
    top: 0;
    left: 0;
  }

  &::after {
    background: linear-gradient(-45deg, white 16px, transparent 0),
      linear-gradient(45deg, white 16px, transparent 0);
    bottom: 0;
    left: 0;
  }
`;
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <NavBar />
      </div>
      <div className="ticket"></div>
      <Routes>
        <Route path="/" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
