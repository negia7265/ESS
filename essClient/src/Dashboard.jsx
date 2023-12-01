import React, { useState } from 'react';
import styled from 'styled-components';
import { nanoid } from 'nanoid'
import Candidates from './Candidates';
import axios from 'axios';
const Container = styled.div`
  align-items: center;
  justify-content: center;
  padding:2em;
`;
const Table=styled.table`
width:40vw;
align-items:center;
justify-content:center;
text-align:center;
`
const Dropzone = styled.div`
  width: 40vw;
  height: 20vh;
  border: 1px dashed #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  position:relative;
  &:hover{
    opacity:0.8;
  }
  border-radius:1em;
  background-color: #f0f0f0;
`;

const FileInput = styled.input`
opacity:0;
position: absolute;
width: 100%;
height: 100%;
top: 0;
left: 0;
cursor: pointer;
`;

const Button = styled.button`
  margin-top: 10px;
  background-color:indigo;
  height:3em;
  width:8em;
  color:white;
  font-weight:bold;
  font-size:1em;
  border-radius:1em;
  cursor:pointer;
`;
const Delete=styled.button`
 cursor:pointer;
 font-size:1em;
 background:transparent;
 padding:1em;
 overlow:hidden;
`;

const SplitScreen = styled.div`
  display: flex;
  height: 100vh;
`;

const LeftPane = styled.div`
  overflow-y:auto;
  background-color: #f0f0f0;
`;

const RightPane = styled.div`
  overflow-y: auto;
  background-color: #ffffff;
`;


const FileContainer = styled.div`
  width: 40vw;
  margin-top:0.5em;
  height: 10vh;
  border: 1px solid grey;
  display:flex;
  align-items: center;
  justify-content:space-between;
  border-radius: 1em;
`;


const App = () => {
    const [selectedfile, setSelectedFile] = useState([]);
    const [essData,setessData]=useState({
      'date':new Set(),
      'distance':new Set(),
      'amount':new Set(),
      'source_address':new Set(),
      'destination_address':new Set()
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
              id: nanoid() ,
              filename: e.target.files[i].name,
              filetype: e.target.files[i].type,
              file_content:e.target.files[i],
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
  
    const fileUploadSubmit = (e) => {
      e.preventDefault();    
      setessData(prevState => ({
        ...prevState,
        source_address: new Set(),
        destination_address: new Set(),
        amount: new Set(),
        date: new Set(),
        distance: new Set(),
      }));

      if (selectedfile.length > 0) {
        const formData = new FormData();
        selectedfile.map((file)=>{
          formData.append("file", file.file_content);      
                if(file.filetype=='application/pdf'){
                  axios.post("http://127.0.0.1:5000/parse_invoice/api/pdf",formData, {
                    headers: {
                      "Content-Type": "multipart/form-data",
                    },
                  }).then((response) => {
                      setessData((prevState) => {
                        let updatedState = { ...prevState };
                        updatedState.source_address=response.data.address
                        updatedState.destination_address=(response.data.address)
                        updatedState.amount=(response.data.amount)
                        updatedState.date=response.data.date
                        updatedState.distance=response.data.distance
                        return updatedState
                      });
                  })
                }else if(file.filetype.startsWith('image')){
                  axios.post("http://localhost:8080/upload",formData, {
                    headers: {
                      "Content-Type": "multipart/form-data",
                    },
                  }).then((response) => {
                      setessData((prevState) => {
                        let updatedState = { ...prevState };
                        updatedState.source_address=response.data.address
                        updatedState.destination_address=(response.data.address)
                        updatedState.amount=(response.data.amount)
                        updatedState.date=response.data.date
                        updatedState.distance=response.data.distance
                        return updatedState
                      });

                  })
                }
        })           
        setSelectedFile([]);
      } else {
        alert("Please select file");
      }
    };
  return (
    <SplitScreen>
      <LeftPane>
        <Candidates candidateType={'Date'} candidateValues={Array.from(essData.date)}/>
        <Candidates candidateType={'Distance'} candidateValues={Array.from(essData.distance)}/>
        <Candidates candidateType={'Amount'} candidateValues={Array.from(essData.amount)}/>
        <Candidates candidateType={'Source Address'} candidateValues={Array.from(essData.source_address)}/>
        <Candidates candidateType={'Destination Address'} candidateValues={Array.from(essData.destination_address)}/>
      </LeftPane>
      <RightPane>
      <Container>
        <Dropzone>
              <FileInput type="file" multiple onChange={InputChange} />
              <img src='file.svg' height='40' width='40'/>
              <br/>
              <p><strong>Click to upload</strong> or drag and drop
              <br/>
              upto 4 images/pdf, 3MB per file
              </p>
         </Dropzone>   
        <Button onClick={fileUploadSubmit}>Upload</Button>
        {selectedfile.map((data) => {
                          const { id, filename, fileimage, filesize } = data;
                           return  <FileContainer key={id} id={id}>
                            <img src='cool_file.svg' height='40'/>
                            <div>
                                {filename} <br/>
                                {filesize} 
                            </div>
                            <Delete
                            type="button"
                            onClick={() => deleteSelectFile(id)}
                            >
                                ❌                                
                            </Delete>
                            </FileContainer>
                        })}
    </Container>
      </RightPane>
    </SplitScreen>
  );
};


export default App;