import React, { useState } from "react";
import "./Form.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import styled from "styled-components";
export const Form = (props) => {
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
  return (
    <div className="formContainer" style={{ width: "100%", height: "auto" }}>
      <div class="container" style={{ width: "100vh", height: "95vh" }}>
        <form>
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
                <i class="fa fa-calendar" aria-hidden="true"></i>
              </div>
            </div>
            <div
              style={{ marginTop: "35px", marginBottom: "35px" }}
              class="input-group input-group-icon"
            >
              <input
                type="email"
                style={{ fontSize: "2vh" }}
                placeholder="Distance"
                value={distance}
                onChange={handleDistance}
              />
              <div class="input-icon">
                <i class="fa fa-car" aria-hidden="true"></i>
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
                <i class="fa fa-inr" aria-hidden="true"></i>
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
                <i class="fa fa-compass" aria-hidden="true"></i>
              </div>
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
                <i class="fa fa-compass" aria-hidden="true"></i>
              </div>
            </div>
          </div>

          <div class="input-group">
            <input
              id="card-1"
              type="radio"
              name="Travel Purpose"
              value="Home to Office"
              checked="true"
            />
            <label for="card-1">
              <span style={{ cursor: "pointer" }}>Home to Office</span>
            </label>
            <input
              id="card-2"
              type="radio"
              name="Travel Purpose"
              value="Office to Home"
            />
            <label for="card-2">
              <span style={{ cursor: "pointer" }}>Office to Home</span>
            </label>
          </div>
          <div className="buttonContainer">
            <Button>Submit</Button>
          </div>
        </form>
      </div>
    </div>
  );
};
