import React from "react";
import ReactDOM from "react-dom/client";
import { Routes, Route } from "react-router-dom";
import "./ESS.css";
import Dashboard from "./Dashboard";
import NavBar from "./Navbar";
import { BrowserRouter } from "react-router-dom";
import { DNA, Hourglass } from "react-loader-spinner";
import { Loader } from "./Loader";
import { MainApp } from "./MainApp";
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <MainApp />
  </React.StrictMode>
);
