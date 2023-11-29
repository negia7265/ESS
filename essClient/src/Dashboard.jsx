import React, { useState } from 'react';
import styled from 'styled-components';
import { nanoid } from 'nanoid'

const Container = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(to right, #003366, #004080, #0059b3, #0073e6);
`;

const Dropzone = styled.div`
  width: 40vw;
  height: 60vh;
  border: 1px dashed #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  position:relative;
  &:hover{
    opacity:0.8;
  }
  border-radius:1em;
  background-color:grey;
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
`;

const MultipleFileUpload = () => {
  const [files, setFiles] = useState([]);
  const [selectedfile, setSelectedFile] = useState([]);
  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const filesizes = (bytes, decimals = 2) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  };

  const InputChange = (e) => {
    let images = [];
    for (let i = 0; i < e.target.files.length; i++) {
      images.push(e.target.files[i]);
      let reader = new FileReader();
      let file = e.target.files[i];
      reader.onloadend = () => {
        setSelectedFile((prevValue) => [
          ...prevValue,
          {
            id: nanoid() ,
            filename: e.target.files[i].name,
            filetype: e.target.files[i].type,
            fileimage: reader.result,
            datetime: e.target.files[i].lastModifiedDate.toLocaleString("en-IN"),
            filesize: filesizes(e.target.files[i].size),
          },
        ]);
      };
      if (e.target.files[i]) {
        reader.readAsDataURL(file);
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
    e.target.reset();
    if (selectedfile.length > 0) {
      setFiles((prevValue) => [...prevValue, ...selectedfile]);
      setSelectedFile([]);
    } else {
      alert("Please select file");
    }
  };

  const deleteFile = (id) => {
    if (window.confirm("Are you sure you want to delete this Image?")) {
      const result = Files.filter((data) => data.id !== id);
      setFiles(result);
    }
  };
  return (
    <Container>
      <Dropzone>
              <FileInput type="file" multiple onChange={handleFileChange} />
              <img src='file.svg' height='40' width='40'/>
              <br/>
              <p><strong>Click to upload</strong> or drag and drop
              <br/>
              upto 4 images/pdf, 3MB per file
              </p>
      </Dropzone>
        
      {/* <Button onClick={handleUpload}>Upload</Button> */}
    </Container>
  );
};

export default MultipleFileUpload;
// const App = () => {
//   const [selectedfile, setSelectedFile] = useState([]);
//   const [Files, setFiles] = useState([]);

//   const filesizes = (bytes, decimals = 2) => {
//     if (bytes === 0) return "0 Bytes";
//     const k = 1024;
//     const dm = decimals < 0 ? 0 : decimals;
//     const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
//     const i = Math.floor(Math.log(bytes) / Math.log(k));
//     return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
//   };

//   const InputChange = (e) => {
//     let images = [];
//     for (let i = 0; i < e.target.files.length; i++) {
//       images.push(e.target.files[i]);
//       let reader = new FileReader();
//       let file = e.target.files[i];
//       reader.onloadend = () => {
//         setSelectedFile((prevValue) => [
//           ...prevValue,
//           {
//             id: shortid.generate(),
//             filename: e.target.files[i].name,
//             filetype: e.target.files[i].type,
//             fileimage: reader.result,
//             datetime: e.target.files[i].lastModifiedDate.toLocaleString("en-IN"),
//             filesize: filesizes(e.target.files[i].size),
//           },
//         ]);
//       };
//       if (e.target.files[i]) {
//         reader.readAsDataURL(file);
//       }
//     }
//   };

//   const deleteSelectFile = (id) => {
//     if (window.confirm("Are you sure you want to delete this Image?")) {
//       const result = selectedfile.filter((data) => data.id !== id);
//       setSelectedFile(result);
//     }
//   };

//   const fileUploadSubmit = (e) => {
//     e.preventDefault();
//     e.target.reset();
//     if (selectedfile.length > 0) {
//       setFiles((prevValue) => [...prevValue, ...selectedfile]);
//       setSelectedFile([]);
//     } else {
//       alert("Please select file");
//     }
//   };

//   const deleteFile = (id) => {
//     if (window.confirm("Are you sure you want to delete this Image?")) {
//       const result = Files.filter((data) => data.id !== id);
//       setFiles(result);
//     }
//   };

//   return (
//       <div className="row justify-content-center m-0">
//         <div className="col-md-6">
//           <div className="card mt-5">
//             <div className="card-body">
//               <div className="kb-data-box">
//                 <div className="kb-modal-data-title">
//                   <div className="kb-data-title">
//                     <h6>Multiple File Upload With Preview</h6>
//                   </div>
//                 </div>
//                 <form onSubmit={fileUploadSubmit}>
//                   <div className="kb-file-upload">
//                     <div className="file-upload-box">
//                       <input
//                         type="file"
//                         id="fileupload"
//                         className="file-upload-input"
//                         onChange={InputChange}
//                         multiple
//                       />
//                       <span>
//                         Drag and drop or{" "}
//                         <span className="file-link">Choose your files</span>
//                       </span>
//                     </div>
//                   </div>
//                   <div className="kb-attach-box mb-3">
//                     {selectedfile.map((data) => {
//                       const { id, filename, fileimage, datetime, filesize } = data;
//                       return (
//                         <div className="file-atc-box" key={id}>
//                           {filename.match(/.(jpg|jpeg|png|gif|svg)$/i) ? (
//                             <div className="file-image">
//                               {" "}
//                               <img src={fileimage} alt="" />
//                             </div>
//                           ) : (
//                             <div className="file-image">
//                               <i className="far fa-file-alt"></i>
//                             </div>
//                           )}
//                           <div className="file-detail">
//                             <h6>{filename}</h6>
//                             <p></p>
//                             <p>
//                               <span>Size : {filesize}</span>
//                               <span className="ml-2">
//                                 Modified Time : {datetime}
//                               </span>
//                             </p>
//                             <div className="file-actions">
//                               <button
//                                 type="button"
//                                 className="file-action-btn"
//                                 onClick={() => deleteSelectFile(id)}
//                               >
//                                 Delete
//                               </button>
//                             </div>
//                           </div>
//                         </div>
//                       );
//                     })}
//                   </div>
//                   <div className="kb-buttons-box">
//                     <button
//                       type="submit"
//                       className="btn btn-primary form-submit"
//                     >
//                       Upload
//                     </button>
//                   </div>
//                 </form>
//                 {Files.length > 0 && (
//                   <div className="kb-attach-box">
//                     <hr />
//                     {Files.map((data, index) => {
//                       const { id, filename, fileimage, datetime, filesize } = data;
//                       return (
//                         <div className="file-atc-box" key={index}>
//                           {filename.match(/.(jpg|jpeg|png|gif|svg)$/i) ? (
//                             <div className="file-image">
//                               {" "}
//                               <img src={fileimage} alt="" />
//                             </div>
//                           ) : (
//                             <div className="file-image">
//                               <i className="far fa-file-alt"></i>
//                             </div>
//                           )}
//                           <div className="file-detail">
//                             <h6>{filename}</h6>
//                             <p>
//                               <span>Size : {filesize}</span>
//                               <span className="ml-3">
//                                 Modified Time : {datetime}
//                               </span>
//                             </p>
//                             <div className="file-actions">
//                               <button
//                                 className="file-action-btn"
//                                 onClick={() => deleteFile(id)}
//                               >
//                                 Delete
//                               </button>
//                               <a
//                                 href={fileimage}
//                                 className="file-action-btn"
//                                 download={filename}
//                               >
//                                 Download
//                               </a>
//                             </div>
//                           </div>
//                         </div>
//                       );
//                     })}
//                   </div>
//                 )}
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>
//   );
// };
// export default App;