import React from "react";
import ReactDOM from "react-dom/client";
import ESS from './ESS';
import { BrowserRouter } from "react-router-dom";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
     
     <ESS/>
    </BrowserRouter>
  </React.StrictMode>
);
