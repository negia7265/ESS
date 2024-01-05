import React, { useEffect, useState } from "react";
import "./Form.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import styled from "styled-components";
import Swal from "sweetalert2";
import Alert from "@mui/material/Alert";
export const Form = ({ formData, setloadPreview, setloadForm, essStatus }) => {
  const [date, setDate] = useState("");
  const [distance, setDistance] = useState("");
  const [amount, setAmount] = useState("");
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [travelReason, settravelReason] = useState("");
  const [threshHold, setThreshHold] = useState(10);
  const [serviceStatus, setServiceStatus] = useState(false);
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
  useEffect(() => {
    setDate(formData.date);

    setDistance(formData.distance);

    setAmount(formData.amount);

    setSource(formData.sourceAddress);

    setDestination(formData.destinationAddress);
  }, [formData]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      date,
      distance,
      amount,
      sourceAddress: source,
      destinationAddress: destination,
      travelReason,
      status: essStatus.status,
    };
    if (
      data.length == 0 ||
      distance.length == 0 ||
      amount.length == 0 ||
      source.length == 0 ||
      destination.length == 0 ||
      travelReason.length == 0
    ) {
      Swal.fire({
        icon: "error",
        title: "Missing Fields!!",
      });
    } else {
      Swal.fire({
        icon: "success",
        title: "ESS Service Approved",
      });
      setTimeout(() => {
        setloadForm(false);
        setloadPreview(false);
        Swal.close();
      }, 3000);
    }
  };
  const handleTravelReason = (e) => {
    settravelReason(e.target.value);
  };
  const handleFormClick = () => {
    console.log("Form clicked");
  };
  console.log(essStatus);
  useEffect(() => {
    console.log(essStatus);
    if (essStatus.status === "ESS_Denied") setServiceStatus(false);
    else setServiceStatus(true);
  }, [formData]);
  useEffect(() => {
    // Set the initial travel reason based on essStatus when component mounts
    settravelReason(essStatus.direction);
  }, [essStatus]);

  return (
    <div className="formContainer" style={{ width: "100%", height: "auto" }}>
      <div class="container" style={{ width: "100vh", height: "115vh" }}>
        {serviceStatus ? (
          <Alert variant="filled" severity="success">
            Eligible for ESS Service
          </Alert>
        ) : (
          <Alert variant="filled" severity="error">
            Not Eligible for ESS Service
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <div class="row">
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
              value="home_to_office"
              checked={travelReason === "home_to_office"}
              onChange={handleTravelReason}
            />
            <label for="card-1">
              <span style={{ cursor: "pointer" }}>Home to Office</span>
            </label>
            <input
              id="card-2"
              type="radio"
              name="Travel Purpose"
              value="office_to_home"
              checked={travelReason === "office_to_home"}
              onChange={handleTravelReason}
            />
            <label for="card-2">
              <span style={{ cursor: "pointer" }}>Office to Home</span>
            </label>
          </div>
          <div className="buttonContainer">
            <Button onClick={handleFormClick} type="submit">
              Submit
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};
