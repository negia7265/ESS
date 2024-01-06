import React, { useState } from "react";
import styled from "styled-components";
import { nanoid } from "nanoid";
import Candidates from "./Candidates";
import axios from "axios";
import { convertPdfToImages, readFileData } from "./pdf2img";
import Preview from "./Preview";
import { Form } from "./Form";
import AttachFileOutlinedIcon from "@mui/icons-material/AttachFileOutlined";
import JSZip from "jszip";
import { DNA, Hourglass } from "react-loader-spinner";

const Container = styled.div`
  align-items: center;
  justify-content: center;
  padding: 2em;
  width: 100%;
`;
const Dropzone = styled.div`
  width: 100%;
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
  width: 100%;
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
  width: 70vh;
  margin: 10px;
  overflow: hidden;
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
  background: ${(props) => props.Color};

  color: #fff;
  border: none;
  position: relative;
  height: 60px;
  font-size: 1.6em;
  padding: 0 2em;
  cursor: pointer;
  transition: 800ms ease all;
  outline: none;
  width: 100%;
  margin-top: 5vh;
  &:hover {
    background: #fff;
    color: ${(props) => props.Color};
  }

  &:before,
  &:after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    height: 2px;
    width: 0;
    background: ${(props) => props.Color};
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
  //For ESS status and threshold
  const [essStatus, setessStatus] = useState({});
  const [threshold, setThreshold] = useState(274000);
  const [homethreshold, sethomeThreshold] = useState(700);
  const [officeName, setofficeName] = useState(
    "AMR Tech Park II, No. 23 & 24, Hongasandra, Hosur Main Road, Bengaluru, Karnataka 560068"
  );
  const [homeAddress, sethomeAddress] = useState(
    "249, 14th Main Rd, Sector 7, HSR Layout, Bengaluru, Karnataka 560102"
  );
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
  // Slide For Email
  const [daysAgo, setdaysAgo] = useState(0);
  //For Email Selecting Box
  const [loademailSelectTable, setloademailSelectTable] = useState(false);
  const [emailDetails, setEmailDetails] = useState([]);
  const [blobArray, setblobArray] = useState([]);
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

  //Function to return a list of blobs from multiple pdfs
  const extractZipData = async (zipBlob) => {
    try {
      // Create a new instance of JSZip
      const zip = new JSZip();

      // Load the zip file
      const zipFile = await zip.loadAsync(zipBlob);

      // Extract data from each file in the zip
      const extractedData = await Promise.all(
        Object.keys(zipFile.files).map(async (filename) => {
          const file = zipFile.files[filename];
          const fileData = await file.async("blob");
          const pdfBlob = new Blob([fileData], { type: "application/pdf" });
          return pdfBlob;
        })
      );
      const reversedData = extractedData.reverse();
      return reversedData;
    } catch (error) {
      console.error("Error extracting zip data:", error);
      throw error;
    }
  };

  const handleFormClick = (e) => {
    setTimeout(() => {
      console.log("Form submitted");
    }, 2000);
  };

  const handleEmailSelect = (blob) => {
    // setloadPreview(true);
    // setloadForm(false);
    // setSourceAddress({});
    // setDestinationAddress({});
    // setAmount({});
    // setDate({});
    // setDistance({});
    // setInvoiceImages([]);
    // setPreview(true);
    props.setLoading(true);
    setloademailSelectTable(false);
    console.log(blob);
    // const formData = new FormData();

    // Append the Blob as a file with the key 'file'
    const formData = new FormData();
    formData.append("file", blob, "latest_attachment.pdf");
    convertPdfToImages(blob).then((data) => {
      setInvoiceImages((prevImages) => [...prevImages, ...data]);
    });
    axios
      .post("http://localhost:5000/parse_invoice/api", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        // props.setLoading(false);
        // const valuesArray = Object.keys(response.data.address);
        const sourceAddressCleaned = response.data.src;
        const destinationAddressCleaned = response.data.dest;

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
        const threshData = {
          source_name: response.data.src,
          destination_name: response.data.dest,
          office_name: officeName,
          threshold: threshold,
          homethreshold: homethreshold,
          homeAddress: homeAddress,
        };
        axios
          .post("http://127.0.0.1:5000/get_threshold_distances", threshData)
          .then((response) => {
            console.log(response.data);
            setessStatus(response.data);
          });
        props.setLoading(false);
      });
    setloadPreview(true);
    setloadForm(false);
    setSourceAddress({});
    setDestinationAddress({});
    setAmount({});
    setDate({});
    setDistance({});
    setInvoiceImages([]);
    setPreview(true);
    setSelectedFile([]);
  };
  const handleEmailClick = async (e) => {
    e.preventDefault();
    // setloadPreview(true);
    // setloadForm(false);
    // setSourceAddress({});
    // setDestinationAddress({});
    // setAmount({});
    // setDate({});
    // setDistance({});
    // setInvoiceImages([]);
    // setPreview(true);
    props.setLoading(true);

    // const form_data = await axios.get("http://127.0.0.1:5000/get_latest_pdf", {
    //   responseType: "arraybuffer",
    // });
    const days = {
      days: daysAgo,
    };

    const form_num_days_data = await axios.post(
      "http://127.0.0.1:5000/get_last_num_days_pdf",
      days,
      {
        responseType: "arraybuffer",
      }
    );
    const invoice_data_last_num_days = await axios.post(
      "http://127.0.0.1:5000/fetch_invoice_data_last_num_days",
      days
    );
    const zipBlob = new Blob([form_num_days_data.data], {
      type: "application/zip",
    });
    // const pdfBlob = new Blob([form_data.data], { type: "application/pdf" });

    const temporary = await extractZipData(zipBlob);
    setblobArray(temporary);
    setEmailDetails(invoice_data_last_num_days.data.invoice_data);
    setloademailSelectTable(true);
    props.setLoading(false);

    // // Create a FormData object
    // const formData = new FormData();

    // // Append the Blob as a file with the key 'file'
    // formData.append("file", pdfBlob, "latest_attachment.pdf");
    // convertPdfToImages(pdfBlob).then((data) => {
    //   setInvoiceImages((prevImages) => [...prevImages, ...data]);
    // });
    // axios
    //   .post("http://localhost:5000/parse_invoice/api", formData, {
    //     headers: {
    //       "Content-Type": "multipart/form-data",
    //     },
    //   })
    //   .then((response) => {
    //     props.setLoading(false);
    //     // const valuesArray = Object.keys(response.data.address);
    //     const sourceAddressCleaned = response.data.src;
    //     const destinationAddressCleaned = response.data.dest;

    //     // console.log(valuesArray[0]);
    //     setSourceAddress((prevState) => {
    //       setFormData((prevState) => {
    //         return {
    //           ...prevState,
    //           sourceAddress: sourceAddressCleaned,
    //         };
    //       });
    //     });
    //     setDestinationAddress((prevState) => {
    //       setFormData((prevState) => {
    //         return {
    //           ...prevState,
    //           destinationAddress: destinationAddressCleaned,
    //         };
    //       });
    //     });
    //     setAmount((prevState) => {
    //       // const max_amount_value = findMaxKey(response.data.amount);
    //       // console.log(max_amount_value);
    //       setFormData((prevState) => {
    //         return {
    //           ...prevState,
    //           amount: response.data.amount,
    //         };
    //       });
    //     });
    //     setDistance((prevState) => {
    //       setFormData((prevState) => {
    //         return {
    //           ...prevState,
    //           distance: response.data.dist,
    //         };
    //       });
    //     });
    //     setDate((prevState) => {
    //       setFormData((prevState) => {
    //         return {
    //           ...prevState,
    //           date: response.data.date,
    //         };
    //       });
    //     });
    //     const threshData = {
    //       source_name: response.data.src,
    //       destination_name: response.data.dest,
    //       office_name: officeName,
    //       threshold: threshold,
    //       homethreshold: homethreshold,
    //       homeAddress: homeAddress,
    //     };
    //     axios
    //       .post("http://127.0.0.1:5000/get_threshold_distances", threshData)
    //       .then((response) => {
    //         console.log(response.data);
    //         setessStatus(response.data);
    //       });
    //   });

    // setSelectedFile([]);
    // e.target.value = null;
  };

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
        console.log(file.file_content);
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
          .post("http://localhost:5000/parse_invoice/api", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            props.setLoading(false);
            console.log(response);
            // const valuesArray = Object.keys(response.data.address);
            const sourceAddressCleaned = response.data.src;
            const destinationAddressCleaned = response.data.dest;
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
            const threshData = {
              source_name: response.data.src,
              destination_name: response.data.dest,
              office_name: officeName,
              threshold: threshold,
              homethreshold: homethreshold,
              homeAddress: homeAddress,
            };
            axios
              .post("http://127.0.0.1:5000/get_threshold_distances", threshData)
              .then((response) => {
                console.log(response.data);
                setessStatus(response.data);
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
  const handleFormSelectClick = () => {
    setloadForm(true);
    setloadPreview(false);
    setAuthState("signup");
  };
  const handlePreviewClick = () => {
    setloadForm(false);
    setloadPreview(true);
    setAuthState("login");
  };
  const handleSliderChange = (e) => {
    setdaysAgo(e.target.value);
  };

  //Email Selecting Box getting time lag when creating a separat Component Will try later

  const EmailSelect = () => {
    const handleSelect = (i) => {
      handleEmailSelect(blobArray[i]);
    };
    return (
      <div class="container">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">No</th>
              <th scope="col">Subject</th>
              <th scope="col">Sender's id</th>
              <th scope="col">Date Received</th>
              <th scope="col">Time Received</th>
              <th scope="col" colspan="2">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {emailDetails.length > 0 ? (
              emailDetails.map((email, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>{email.subject}</td>
                  <td>{email.sender_address}</td>
                  <td>{email.date_received}</td>
                  <td>{email.time_received}</td>
                  <td className="text-right">
                    <button
                      onClick={() => handleSelect(i)}
                      className="btn btn-outline-warning"
                    >
                      Select
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7}>No Emails</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "center" }}>
        {!loademailSelectTable && !loadPreview && !loadForm && (
          <>
            <div style={{ width: "90%", maxWidth: "500px" }}>
              <div
                style={{
                  margin: "5px",
                  display: "flex",
                  flexDirection: "column",
                }}
              >
                <h3>{`Fetch invoices from ${daysAgo} days ago`}</h3>
                <input
                  id="changeSize"
                  type="range"
                  min="0"
                  max="30"
                  style={{ background: "grey" }}
                  defaultValue={0}
                  //disabled={isRunning ? "disabled" : null}
                  onChange={handleSliderChange}
                />
                <StyledButton onClick={handleEmailClick} Color="#ffc632">
                  Use Email
                </StyledButton>
              </div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  margin: "9px",
                }}
              >
                <h2>OR</h2>
              </div>
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
                <StyledButton Color="#3066b1" onClick={fileUploadSubmit}>
                  Upload
                </StyledButton>

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
                      <Delete
                        type="button"
                        onClick={() => deleteSelectFile(id)}
                      >
                        ❌
                      </Delete>
                    </FileContainer>
                  );
                })}
              </div>
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
              <Slide onClick={handleFormSelectClick}>ESS Form</Slide>
              <SliderTab state={authState} />
            </SlideControls>
          </Wrapper>
        </div>
      )}


      {loademailSelectTable ? (
        <EmailSelect />
      ) : (
        !props.loading && (
          <div style={{ marginBottom: "100px" }}>
            {loadPreview ? (
              <div style={{ marginLeft: "5vw", marginRight: "5vw" }}>
                <Preview invoiceImages={invoiceImages} />
              </div>
            ) : loadForm ? (
              <Form
                setloadPreview={setloadPreview}
                handleFormClick={handleFormClick}
                setloadForm={setloadForm}
                formData={formData}
                essStatus={essStatus}
              />
            ) : (
              <div></div>
            )}
          </div>
        )
      )}
      ;
      {/* <EmailSelect
      // emailDetails={emailDetails}
      // blobArray={blobArray}
      // setSelectedBlob={setSelectedBlob}
      // handleEmailSelect={handleEmailSelect}
      /> */}
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
