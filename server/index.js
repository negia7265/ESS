const express = require("express");
require("dotenv").config();
const app = express();
const cors = require("cors");
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
const bcrypt = require("bcrypt");
const mongoose = require("mongoose");
const multer= require('multer')
const axios=require('axios')
mongoose.set("strictQuery", true);

// const User = require("User");
const uri = process.env.URI;
const storage = multer.memoryStorage(); 
const ocr=require('./ocr');
const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/') || file.mimetype === 'application/pdf') {
      cb(null, true);
    } else {
      cb(new Error('Only PDF or images are allowed!'), false);
    }
  },
  limits: {
    files:4, // Maximum number of files in a single request
    fileSize:7340032  // 1024 X 1024 X 7 MB
  },
});


// mongoose
//   .connect(uri)
//   .then(() => console.log("Connected to MongoDB Atlas!"))
//   .catch((err) => console.error("Error connecting to MongoDB Atlas:", err));

// app.post("/signup", async (req, res) => {
//   const { name, email, password } = req.body;
//   const data = await User.findOne({ email: email });
//   if (data) {
//     res.send({ status: 3 });
//   } else {
//     const salt = bcrypt.genSaltSync(10);
//     const hashedPassword = bcrypt.hashSync(password, salt);
//     try {
//       const temp = new User({
//         name: name,
//         email: email,
//         password: hashedPassword,
//       });
//       const data = await temp.save();
//     } catch (error) {
//       console.log(error);
//     }
//     res.send({ status: 1 });
//   }
// });

// app.post("/login", async (req, res) => {
//   const { email, password } = req.body;
//   const data = await User.findOne({ email: email });
//   if (data) {
//     const temp = bcrypt.compareSync(password, data.password);
//     if (temp) {
//       console.log(temp);
//       res.send({ status: 2 });
//     } else {
//       res.send({ status: -1 });
//     }
//   } else {
//     res.send({ status: 0 });
//   }
// });

app.post('/upload',async (req,res)=>{
  upload.array('files')(req, res, (err) => {
    if (err instanceof multer.MulterError) {
      if (err) {
        res.send(err)
      }
    } 
    const files = req.files;
    if (!files) {
      return res.status(400).send('No files were uploaded.');
    }
    ocr(files).then((f)=>{
       console.log(f)
    }).catch((error) => {
      console.error(error);
    });
    // axios.post('http://127.0.0.1:5000/extractInvoice/',ocr(files)).then((data)=>{
    //   res.send(data)
    // })
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
