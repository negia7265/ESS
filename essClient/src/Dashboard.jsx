import React, { useState } from "react";
import styled from "styled-components";
import { nanoid } from "nanoid";
import Candidates from "./Candidates";
import axios from "axios";
import { convertPdfToImages, readFileData } from "./pdf2img";
import Preview from "./Preview";
import { Form } from "./Form";
import AttachFileOutlinedIcon from "@mui/icons-material/AttachFileOutlined";

import { DNA, Hourglass } from "react-loader-spinner";
const Container = styled.div`
  align-items: center;
  justify-content: center;
  padding: 2em;
  width: 100%;
`;
const Dropzone = styled.div`
  width: 40vw;
  height: 20vh;
  border: 5px dashed #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  &:hover {
    opacity: 0.8;
  }
  border-radius: 1em;
  background-color: transparent;
`;

const FileInput = styled.input`
  opacity: 0;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  cursor: pointer;
`;

const Button = styled.button`
  margin-top: 10px;
  background-color: indigo;
  height: 3em;
  width: 8em;
  color: white;
  font-weight: bold;
  font-size: 1em;
  border-radius: 1em;
  cursor: pointer;
`;
const Delete = styled.button`
  cursor: pointer;
  font-size: 1em;
  background: transparent;
  padding: 1em;
`;

const SplitScreen = styled.div`
  display: flex;
  height: 93vh;
  overflow: hidden;
`;

const LeftPane = styled.div`
  overflow-y: auto;
  background-color: #f0f0f0;
  width: 40vw;
`;

const RightPane = styled.div`
  overflow-y: auto;
  background-color: #f0f0f0;
  width: 60vw;
`;

const FileContainer = styled.div`
  width: 40vw;
  margin-top: 0.5em;
  height: 7vh;
  border: 0.5px solid grey;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 0.4em;
  font-weight: bold;
`;
const ImageContainer = styled.div`
   {
    height: 60vh;
    padding: 0;
  }
`;
const Image = styled.img`
   {
    width: 100vw;
    pdding: 0;
  }
`;

//Dealing with Sliding Tab
const Wrapper = styled.div`
  overflow: hidden;
  min-width: 100vh;
  min-height: 25vh;
  background: #fff;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0px 15px 20px rgba(0, 0, 0, 0.1);
`;

const TitleText = styled.div`
  display: flex;
  width: 200%;
`;

const Title = styled.div`
  width: 50%;
  font-size: 35px;
  font-weight: 600;
  text-align: center;
  transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);

  &:first-child {
    margin-left: ${(props) => (props.state == "login" ? "-50%" : "0%")};
  }
`;

const SlideControls = styled.div`
  position: relative;
  display: flex;
  height: 50px;
  width: 100%;
  overflow: hidden;
  margin: 30px 0 10px 0;
  justify-content: space-between;
  border: 1px solid lightgrey;
  border-radius: 15px;
`;

const Slide = styled.label`
  height: 100%;
  width: 100%;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  line-height: 48px;
  cursor: pointer;
  z-index: 1;
  transition: all 0.6s ease;
  &:last-child {
    color: #000;
  }
  color: ${(props) => (props.state == "login" ? "white" : "black")};
`;

const SliderTab = styled.div`
  position: absolute;
  height: 100%;
  width: 50%;
  left: 0;
  z-index: 0;
  border-radius: 15px;
  transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  background: -webkit-linear-gradient(left, #003366, #004080, #0059b3, #0073e6);
  ${(props) => props.state != "login" && "left: 50%"};
`;
//Styled components for the File Upload Button
export const StyledButton = styled.button`
  background: #3066b1;
  color: #fff;
  border: none;
  position: relative;
  height: 60px;
  font-size: 1.6em;
  padding: 0 2em;
  cursor: pointer;
  transition: 800ms ease all;
  outline: none;
  min-width: 83vh;
  margin-top: 2vh;
  &:hover {
    background: #fff;
    color: #3066b1;
  }

  &:before,
  &:after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    height: 2px;
    width: 0;
    background: #3066b1;
    transition: 400ms ease all;
  }

  &:after {
    right: inherit;
    top: inherit;
    left: 0;
    bottom: 0;
  }

  &:hover:before,
  &:hover:after {
    width: 100%;
    transition: 800ms ease all;
  }
`;
const App = (props) => {
  const [selectedfile, setSelectedFile] = useState([]);
  const [date, setDate] = useState({});
  const [distance, setDistance] = useState({});
  const [amount, setAmount] = useState({});
  const [sourceAddress, setSourceAddress] = useState({});
  const [destinationAddress, setDestinationAddress] = useState({});
  const [invoiceImages, setInvoiceImages] = useState([]);
  const [preview, setPreview] = useState(false);

  //For switching between the form and Preview
  const [loadPreview, setloadPreview] = useState(false);
  const [loadForm, setloadForm] = useState(false);
  const [formData, setFormData] = useState({
    sourceAddress: "",
    destinationAddress: "",
    amount: "",
    date: "",
    distance: "",
  });
  const filesizes = (bytes, decimals = 2) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    const dm = decimals < 0 ? 0 : decimals;
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  };

  const InputChange = (e) => {
    for (let i = 0; i < e.target.files.length; i++) {
      let reader = new FileReader();
      let file = e.target.files[i];
      reader.onloadend = () => {
        setSelectedFile((prevValue) => [
          ...prevValue,
          {
            id: nanoid(),
            filename: e.target.files[i].name,
            filetype: e.target.files[i].type,
            file_content: e.target.files[i],
            filesize: filesizes(e.target.files[i].size),
          },
        ]);
      };
      if (e.target.files[i]) {
        reader.readAsArrayBuffer(file);
      }
    }
  };

  const deleteSelectFile = (id) => {
    if (window.confirm("Are you sure you want to delete this Image?")) {
      const result = selectedfile.filter((data) => data.id !== id);
      setSelectedFile(result);
    }
  };

  //A function to return the key with the highest value!! will be using this when creating form data from the API returned data.
  // function findMaxKey(obj) {
  //   let maxKey = null;
  //   let maxValue = Number.NEGATIVE_INFINITY;

  //   for (const key in obj) {
  //     if (obj.hasOwnProperty(key) && typeof obj[key] === "number") {
  //       if (obj[key] > maxValue) {
  //         maxValue = obj[key];
  //         maxKey = key;
  //       }
  //     }
  //   }

  //   return maxKey;
  // }

  const fileUploadSubmit = (e) => {
    e.preventDefault();
    setloadPreview(true);
    setloadForm(false);
    setSourceAddress({});
    setDestinationAddress({});
    setAmount({});
    setDate({});
    setDistance({});
    setInvoiceImages([]);
    setPreview(true);
    props.setLoading(true);
    if (selectedfile.length > 0) {
      const formData = new FormData();
      selectedfile.map((file) => {
        if (file.filetype == "application/pdf") {
          convertPdfToImages(file.file_content).then((data) => {
            setInvoiceImages((prevImages) => [...prevImages, ...data]);
          });
        } else {
          readFileData(file.file_content).then((data) => {
            setInvoiceImages((prevImages) => [...prevImages, data]);
          });
        }
        formData.append("file", file.file_content);
        axios
          .post("http://127.0.0.1:5000/parse_invoice/api", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            props.setLoading(false);
            console.log(response);
            // const valuesArray = Object.keys(response.data.address);
            const sourceAddressCleaned = response.data.src;
            const destinationAddressCleaned = response.data.dest
            // console.log(valuesArray[0]);
            setSourceAddress((prevState) => {
              setFormData((prevState) => {
                return {
                  ...prevState,
                  sourceAddress: sourceAddressCleaned,
                };
              });
            });
            setDestinationAddress((prevState) => {
              setFormData((prevState) => {
                return {
                  ...prevState,
                  destinationAddress: destinationAddressCleaned,
                };
              });
            });
            setAmount((prevState) => {
              // const max_amount_value = findMaxKey(response.data.amount);
              // console.log(max_amount_value);
              setFormData((prevState) => {
                return {
                  ...prevState,
                  amount: response.data.amount,
                };
              });
            });
            setDistance((prevState) => {
              setFormData((prevState) => {
                return {
                  ...prevState,
                  distance: response.data.dist,
                };
              });
            });
            setDate((prevState) => {
              setFormData((prevState) => {
                return {
                  ...prevState,
                  date: response.data.date,
                };
              });
            });
          });
      });
      setSelectedFile([]);
      e.target.value = null;
    } else {
      alert("Please select file");
    }
  };

  //Dealing with Sliding tab
  const [authState, setAuthState] = useState("login");
  const handleFormClick = () => {
    setloadForm(true);
    setloadPreview(false);
    setAuthState("signup");
  };
  const handlePreviewClick = () => {
    setloadForm(false);
    setloadPreview(true);
    setAuthState("login");
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "center" }}>
        {!loadPreview && !loadForm && (
          <>
            <div style={{ display: "flex", flexDirection: "column" }}>
              <Dropzone>
                <FileInput
                  type="file"
                  multiple
                  onChange={InputChange}
                  accept=".pdf,image/*"
                />
                <img src="file.svg" height="40" width="40" />
                <br />
                <p>
                  <strong>Click to upload</strong> or drag and drop
                  <br />
                  upto 4 images/pdf, 3MB per file
                </p>
              </Dropzone>
              <StyledButton onClick={fileUploadSubmit}>Upload</StyledButton>

              {/* <Hourglass
                visible={true}
                height="120"
                width="120"
                ariaLabel="hourglass-loading"
                wrapperStyle={{}}
                wrapperClass=""
                colors={["#306cce", "#72a1ed"]}
              /> */}
              {selectedfile.map((data) => {
                const { id, filename, fileimage, filesize } = data;
                return (
                  <FileContainer key={id} id={id}>
                    {/* <img src="cool_file.svg" height="40" /> */}
                    <AttachFileOutlinedIcon />
                    <div>
                      {filename} <br />
                      {filesize}
                    </div>
                    <Delete type="button" onClick={() => deleteSelectFile(id)}>
                      ❌
                    </Delete>
                  </FileContainer>
                );
              })}
            </div>
          </>
        )}
      </div>
      {(loadPreview || loadForm) && (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "5vh",
            marginBottom: "10vh",
          }}
        >
          <Wrapper>
            <TitleText>
              <Title state={authState}>ESS Form</Title>
              <Title state={authState}>Preview</Title>
            </TitleText>
            <SlideControls>
              <Slide onClick={handlePreviewClick}>Preview</Slide>
              <Slide onClick={handleFormClick}>ESS Form</Slide>
              <SliderTab state={authState} />
            </SlideControls>
          </Wrapper>
        </div>
      )}
      {!props.loading && (
        <div>
          {loadPreview ? (
            <div style={{ marginLeft: "59vh" }}>
              <Preview invoiceImages={invoiceImages} />
            </div>
          ) : loadForm ? (
            <Form formData={formData} />
          ) : (
            <div></div>
          )}
        </div>
      )}

      {/* <Preview invoiceImages={invoiceImages} />
      <Form /> */}
      {/* <div style={{ display: "flex", justifyContent: "center" }}>
        {loadPreview && <Preview invoiceImages={invoiceImages} />}
      </div>
      {loadForm && <Form />} */}
    </div>
  );
};
export default App;
