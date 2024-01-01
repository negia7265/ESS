import React, { useState } from "react";
import "./Form.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import styled from "styled-components";
export const Form = ({ formData }) => {
  const [date, setDate] = useState("");
  const [distance, setDistance] = useState("");
  const [amount, setAmount] = useState("");
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [travelReason, settravelReason] = useState("");

  const Button = styled.button`
    width: 100%;
    margin-top: 2vh;
    padding: 1.3em 3em;
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 500;
    color: #000;
    background-color: #fff;
    border: none;
    border-radius: 45px;
    box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease 0s;
    cursor: pointer;
    outline: none;
  `;
  const handleAmount = (e) => {
    setAmount(e.target.value);
  };
  const handleDate = (e) => {
    setDate(e.target.value);
  };
  const handleDistance = (e) => {
    setDistance(e.target.value);
  };
  const handleSource = (e) => {
    setSource(e.target.value);
  };
  const handleDestination = (e) => {
    setDestination(e.target.value);
  };
  if (date?.length == 0) {
    setDate(formData.date);
  }
  if (distance?.length == 0) {
    setDistance(formData.distance);
  }
  if (amount?.length == 0) {
    setAmount(formData.amount);
  }
  if (source?.length == 0) {
    setSource(formData.sourceAddress);
  }
  if (destination?.length == 0) {
    setDestination(formData.destinationAddress);
  }
  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      date,
      distance,
      amount,
      sourceAddress: source,
      destinationAddress: destination,
      travelReason,
    };
    console.log(data);
  };
  const handleTravelReason = (e) => {
    settravelReason(e.target.value);
  };
  return (
    <div className="formContainer" style={{ width: "100%", height: "auto" }}>
      <div class="container" style={{ width: "100vh", height: "100vh" }}>
        <form onSubmit={handleSubmit}>
          <div class="row">
            <h2>ESS FORM</h2>
            <div
              style={{ marginTop: "35px", marginBottom: "35px" }}
              class="input-group input-group-icon"
            >
              <input
                type="text"
                style={{ fontSize: "2vh" }}
                placeholder="Date"
                value={date}
                onChange={handleDate}
              />
              <div class="input-icon">
                <i
                  style={{ color: "#ffc632" }}
                  class="fa fa-calendar"
                  aria-hidden="true"
                ></i>
              </div>
            </div>
            <div
              style={{ marginTop: "35px", marginBottom: "35px" }}
              class="input-group input-group-icon"
            >
              <input
                type="text"
                style={{ fontSize: "2vh" }}
                placeholder="Distance"
                value={distance}
                onChange={handleDistance}
              />
              <div class="input-icon">
                <i
                  style={{ color: "#ffc632" }}
                  class="fa fa-car"
                  aria-hidden="true"
                ></i>
              </div>
            </div>
            <div
              style={{ marginTop: "35px", marginBottom: "35px" }}
              class="input-group input-group-icon"
            >
              <input
                type="text"
                style={{ fontSize: "2vh" }}
                placeholder="Amount"
                value={amount}
                onChange={handleAmount}
              />
              <div class="input-icon">
                <i
                  style={{ color: "#ffc632" }}
                  class="fa fa-inr"
                  aria-hidden="true"
                ></i>
              </div>
            </div>
            <div
              style={{ marginTop: "35px", marginBottom: "35px" }}
              class="input-group input-group-icon"
            >
              <input
                type="text"
                style={{ fontSize: "2vh" }}
                placeholder="Source Address"
                value={source}
                onChange={handleSource}
              />
              <div class="input-icon">
                <i
                  style={{ color: "#ffc632" }}
                  class="fa fa-compass"
                  aria-hidden="true"
                ></i>
              </div>
            </div>
            <div style={{ display: "flex", justifyContent: "center" }}>
              <h3>TO</h3>
            </div>
            <div
              style={{ marginTop: "35px", marginBottom: "35px" }}
              class="input-group input-group-icon"
            >
              <input
                type="text"
                style={{ fontSize: "2vh" }}
                placeholder="Destination Address"
                value={destination}
                onChange={handleDestination}
              />
              <div class="input-icon">
                <i
                  style={{ color: "#ffc632" }}
                  class="fa fa-compass"
                  aria-hidden="true"
                ></i>
              </div>
            </div>
          </div>

          <div class="input-group">
            <input
              id="card-1"
              type="radio"
              name="Travel Purpose"
              value="Home to Office"
              checked={travelReason === "Home to Office"}
              onChange={handleTravelReason}
            />
            <label for="card-1">
              <span style={{ cursor: "pointer" }}>Home to Office</span>
            </label>
            <input
              id="card-2"
              type="radio"
              name="Travel Purpose"
              value="Office to Home"
              checked={travelReason === "Office to Home"}
              onChange={handleTravelReason}
            />
            <label for="card-2">
              <span style={{ cursor: "pointer" }}>Office to Home</span>
            </label>
          </div>
          <div className="buttonContainer">
            <Button type="submit">Submit</Button>
          </div>
        </form>
      </div>
    </div>
  );
};
