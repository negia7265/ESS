import React, { useState } from 'react';
import styled from 'styled-components';
import { nanoid } from 'nanoid'
import Candidates from './Candidates';
import axios from 'axios';
import {convertPdfToImages,readFileData} from './pdf2img';
const Container = styled.div`
  align-items: center;
  justify-content: center;
  padding:2em;
  width:100%;
`;
const Dropzone = styled.div`
  width: 40vw;
  height: 20vh;
  border: 5px dashed #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  position:relative;
  &:hover{
    opacity:0.8;
  }
  border-radius:1em;
  background-color: transparent;
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
`;

const SplitScreen = styled.div`
  display: flex;
  height: 93vh;
  overflow:hidden;
`;

const LeftPane = styled.div`
  overflow-y:auto;
  background-color: #f0f0f0;
  width:40vw;
`;

const RightPane = styled.div`
  overflow-y: auto;
  background-color: #f0f0f0;
  width:60vw;
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
const ImageContainer=styled.div`{
  height:60vh;
  padding:0;
}`
const Image=styled.img`{
  width:100vw;
  pdding:0
}`

const App = () => {
    const [selectedfile, setSelectedFile] = useState([]);
    const [date,setDate]=useState({})
    const [distance,setDistance]=useState({});
    const [amount,setAmount]=useState({})
    const [sourceAddress,setSourceAddress]=useState({});
    const [destinationAddress,setDestinationAddress]=useState({});
    const [invoiceImages,setInvoiceImages]=useState([])
    const [preview,setPreview]=useState(false);
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
      setSourceAddress({});
      setDestinationAddress({});
      setAmount({});
      setDate({});
      setDistance({});
      setInvoiceImages([])
      setPreview(true)
      if (selectedfile.length > 0) {
        const formData = new FormData();
        selectedfile.map((file)=>{
          if(file.filetype=='application/pdf'){
            convertPdfToImages(file.file_content).then((data)=>{
              setInvoiceImages((prevImages)=>[...prevImages, ...data])
            })
          }else{
            readFileData(file.file_content).then((data)=>{
              setInvoiceImages((prevImages) => [...prevImages, data]);
            })
          }
          formData.append("file", file.file_content);      
                if(file.filetype=='application/pdf'){
                  axios.post("http://127.0.0.1:5000/parse_invoice/api/pdf",formData, {
                    headers: {
                      "Content-Type": "multipart/form-data",
                    },
                  }).then((response) => {
                    setSourceAddress((prevState)=>{
                      return {...prevState, ...response.data.address}
                    })
                    setDestinationAddress((prevState)=>{
                      return {...prevState, ...response.data.address}
                    })
                    setAmount((prevState)=>{
                      return {...prevState, ...response.data.amount}
                    })
                    setDistance((prevState)=>{
                    return {...prevState,...response.data.distance}
                     })
                    setDate((prevState)=>{
                      console.log({...prevState,...response.data.date})
                      return {...prevState,...response.data.date}
                    })
                  })
                }else if(file.filetype.startsWith('image')){
                  axios.post("http://localhost:8080/upload",formData, {
                    headers: {
                      "Content-Type": "multipart/form-data",
                    },
                  }).then((response) => {
                    setSourceAddress((prevState)=>{
                      return {...prevState, ...response.data.address}
                    })
                    setDestinationAddress((prevState)=>{
                      return {...prevState, ...response.data.address}
                    })
                    setAmount((prevState)=>{
                      return {...prevState, ...response.data.amount}
                    })
                    setDistance((prevState)=>{
                    return {...prevState,...response.data.distance}
                     })
                    setDate((prevState)=>{
                      return {...prevState,...response.data.date}
                    })
                  }).then(()=>{
                    console.log(date)
                  })
                }
          setLoading(false)
        })           
        setSelectedFile([]);
        e.target.value = null;
      } else {
        alert("Please select file");
      }
    };
    
  return (
    <SplitScreen>
      <LeftPane>
        <Candidates candidateType={'Date'} predictions={Object.entries(date).sort((a,b)=>b[1]-a[1])}/>
        <Candidates candidateType={'Distance'} predictions={Object.entries(distance).sort((a,b)=>b[1]-a[1])}/>
        <Candidates candidateType={'Amount'} predictions={Object.entries(amount).sort((a,b)=>b[1]-a[1])}/>
        <Candidates candidateType={'Source Address'} predictions={Object.entries(sourceAddress).sort((a,b)=>b[1]-a[1])}/>
        <Candidates candidateType={'Destination Address'} predictions={Object.entries(destinationAddress).sort((a,b)=>b[1]-a[1])}/>
      </LeftPane>
      <RightPane>
      <Container>
        {!preview&&<>
        <Dropzone>
              <FileInput type="file" multiple onChange={InputChange} accept=".pdf,image/*" />
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
                </>}
          { invoiceImages.map(image=>{
              return <ImageContainer key={nanoid()} >
                 <Image src={image} alt='invoice image' width={750}/>
              </ImageContainer>
          })}
    </Container>
      </RightPane>
    </SplitScreen>
  );
};


export default App;
