import styled from "styled-components";
import React, { useEffect, useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import Loader from "./Loader";
import './Components/NavbarCSS.css';
import axios from "axios";
import FormData from "form-data";
import { useLocation } from "react-router-dom";
import Dropdown from "./DropDown";
import { Document, Page } from "react-pdf";

import { pdfjs } from "react-pdf";

const Form = styled.form`
  width: 100%;
  margin: 2em;
  background-color: rgba(255, 255, 255, 0.07);
  position: relative;
  border-radius: 10px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 40px rgba(8, 7, 16, 0.6);
  padding: 50px 35px;
  filter: ${(props) => (props.loading == "true" ? "blur(8px)" : "")};
  pointer-events: ${(props) => (props.loading == "true" ? "none" : "")};
`;

const Input = styled.input`
  display: block;
  height: 50px;
  width: 100%;
  background-color: rgba(255, 255, 255, 0.07);
  border-radius: 3px;
  padding: 0 10px;
  margin-top: 8px;
  font-size: 25px;
  font-weight: 300;
  border: 1px solid black;
  color: white;
  font-weight: bold;
  ::placeholder {
    color: #e5e5e5;
  }
`;

const Button = styled.button`
  margin-top: 50px;
  width: 100%;
  background-color: #ffffff;
  border: 1px solid black;
  color: #080710;
  padding: 15px 0;
  font-size:25px;
  font-weight: 600;
  border-radius: 5px;
  cursor: pointer;
`;
const Label = styled.label`
  color: black;
  font-size: 25px;
  font-weight: bold;
  background-color: rgba(255, 255, 255, 0.07);
`;
const Text = styled.div`
  background-color: rgba(255, 255, 255, 0);
  color: orange;
  font-size: 15px;
`;

const Preview = ({ file }) => {
  const [pdfFile, setPdfFile] = useState(null);
  const [numPages, setNumPages] = useState(1);
  const handleLoadPdf = (file) => {
    setPdfFile(URL.createObjectURL(file));
  };
  useEffect(() => {
    if (file) {
      handleLoadPdf(file);
    }
  }, [file]);
  const PrevStyle = {
    height: "400px",
    width: "350px",
    backgroundColor: "rgba(128, 128, 128, 0.4)",
    borderRadius: "7px",
  };
  return (
    <div style={PrevStyle}>
      {pdfFile ? (
        <Document file={pdfFile}></Document>
      ) : (
        <p
          style={{
            backgroundColor: "rgba(128, 128, 128, 0.4)",
            textAlign: "center",
            fontSize: "30px",
            borderRadius: "3px",
          }}
        >
          No PDF selected
        </p>
      )}
    </div>
  );
};

const purposeOptions = ["Home To Office", "Office To Home"];

const ConveyanceForm = (props) => {
  pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const fileTypes = ["PDF"];
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const [distanceOptions, setDistanceOptions] = useState(
    params.get("dis") ? params.get("dis") : []
  );
  const [pickUpAddressOptions, setPickUpAddressOptions] = useState(
    params.get("src") ? params.get("src") : []
  );
  const [destinationAddressOptions, setDestinationAddressOptions] = useState(
    params.get("dest") ? params.get("dest") : []
  );
  const [costOptions, setCostOptions] = useState(
    params.get("amt") ? params.get("amt") : []
  );
  const [dateOptions, setDateOptions] = useState(
    params.get("Date") ? params.get("Date") : []
  );

  const [purpose, setPurpose] = useState("Home To Office");
  const [distance, setDistance] = useState([]);
  const [pickUpAddress, setPickUpAddress] = useState([]);
  const [destinationAddress, setDestinationAddress] = useState([]);
  const [cost, setCost] = useState([]);
  const [date, setDate] = useState(null);

  const handleChange = (file) => {
    console.log(typeof file);
    setLoading(true);
    setFile(file);
    props.setFileData(file);
    const formData = new FormData();
    formData.append("file", file);
    axios
      .post("http://127.0.0.1:5000/extractInvoice/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        setCostOptions(response.data.amount);
        setCost(
          response.data.amount.length > 0
            ? response.data.amount[0]
            : "Select..."
        );
        setDistanceOptions(response.data.Distance);
        setDistance(
          response.data.Distance.length > 0
            ? response.data.Distance[0]
            : "Select..."
        );
        setPickUpAddressOptions(response.data.sourceAddress);
        setPickUpAddress(
          response.data.sourceAddress.length > 0
            ? response.data.sourceAddress[0]
            : "Select..."
        );
        setDestinationAddressOptions(response.data.destinationAddress);
        setDestinationAddress(
          response.data.destinationAddress.length > 0
            ? response.data.destinationAddress[0]
            : "Select..."
        );
        setDateOptions(response.data.Date);
        setDate(
          response.data.Date.length > 0 ? response.data.Date[0] : "Select..."
        );
        setLoading(false);
      })
      .catch((error) => console.error(error));
  };

  return (
    <>
      {/* <Form loading={loading ? "true" : "false"}>
        <Label htmlFor="upload">Upload File Here...</Label>
        <FileUploader
          multiple={false}
          handleChange={handleChange}
          name="file"
          types={fileTypes}
          maxSize={5}
          className="file-uploader"
        /> */}
        {/* <Text>
          {file ? `File name: ${file.name}` : "no files uploaded yet"}
        </Text> */}
        <Label htmlFor="date">Date</Label>

        <Dropdown options={dateOptions} setSelected={setDate} selected={date} />

        <Label htmlFor="purpose">Purpose</Label>
        <Dropdown
          options={purposeOptions}
          setSelected={setPurpose}
          selected={purpose}
        />

        <Label htmlFor="distance">Distance Travelled(km)</Label>

        <Dropdown
          options={distanceOptions}
          setSelected={setDistance}
          selected={distance}
        />

        <Label htmlFor="pickupAddress">Pickup Address</Label>
        <Dropdown
          options={pickUpAddressOptions}
          setSelected={setPickUpAddress}
          selected={pickUpAddress}
        />

        <Label htmlFor="destinationAddress">Destination Address</Label>
        <Dropdown
          options={destinationAddressOptions}
          setSelected={setDestinationAddress}
          selected={destinationAddress}
        />

        <Label htmlFor="cost">Total Cost</Label>
        <Dropdown options={costOptions} setSelected={setCost} selected={cost} />

        <Button>Submit</Button>
      {/* </Form> */}
      {/* <Loader loading={loading} /> */}
    </>
  );
};

const Heading = styled.h1`
  color: black;
  font-family: Oswald;
  justify-content: center;
  align-items: center;
  text-align: center;
  font-size: 40px;
`;

export default ConveyanceForm;
