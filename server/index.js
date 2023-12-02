const express = require("express");
require("dotenv").config();
const app = express();
const cors = require("cors");
app.use(cors());
const fs=require('fs')
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
const multer= require('multer')
const axios=require('axios')
const storage = multer.memoryStorage(); 
const ocr=require('./ocr');
const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image')) {
      cb(null, true);
    } else {
      cb(new Error('only image is allowed!'), false);
    }
  },
  limits: {
    files:1, // Maximum number of files in a single request
    fileSize:7340032  // 1024 X 1024 X 7 MB
  },
});

app.post('/upload',async (req,res)=>{
  upload.single('file')(req, res, (err) => {
    if (err instanceof multer.MulterError) {
        res.send(err)
    } 
    if (!req.file) {
      return res.status(400).send('No invoice image is uploaded.');
    }
    const image = req.file.buffer;
     ocr(image).then((img_data)=>{
       axios.post('http://127.0.0.1:5000/parse_invoice/api/tsv',img_data).then((result)=>{
       res.send(result.data)
       })
    }).catch((error) => {
      console.error(error);
    });
  });
})

app.listen(8080, () => console.log("app listening on http://localhost:8080"));

/*
  status:
  0-User not Found
  1-Sign Up Successful
  2-User Logging in Sucessful
  3-User Already Exist
  -1-Wrong Password
  
  */
