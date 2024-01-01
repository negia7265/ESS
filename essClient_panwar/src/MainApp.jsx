import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import { Routes, Route } from "react-router-dom";
import "./ESS.css";
import Dashboard from "./Dashboard";
import NavBar from "./Navbar";
import { BrowserRouter } from "react-router-dom";
import { DNA, Hourglass } from "react-loader-spinner";
import { Loader } from "./Loader";
export const MainApp = () => {
  const [loading, setLoading] = useState(false);
  return (
    <BrowserRouter>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <NavBar />
      </div>
      <div className="ticket"></div>
      {loading && (
        <div style={{ display: "flex", justifyContent: "center" }}>
          <div
            style={{
              position: "absolute",
              zIndex: 9999,
            }}
          >
            <Loader />
          </div>
        </div>
      )}

      {/* <DNA
        visible={true}
        height="250"
        width="250"
        ariaLabel="dna-loading"
        wrapperStyle={{}}
        wrapperClass="dna-wrapper"
      /> */}
      {/* <Hourglass
        visible={true}
        height="120"
        width="120"
        ariaLabel="hourglass-loading"
        wrapperStyle={{}}
        wrapperClass=""
        colors={["#306cce", "#72a1ed"]}
      /> */}
      <Routes>
        <Route
          path="/"
          element={<Dashboard setLoading={setLoading} loading={loading} />}
        />
      </Routes>
    </BrowserRouter>
  );
};
