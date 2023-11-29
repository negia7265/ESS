const { MailListener } = require("mail-listener5");   
const nodemailer = require('nodemailer');
const FormData = require('form-data');
const axios=require('axios');
const pdfkit=require('pdfkit');
require('dotenv').config()

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL,
    pass: process.env.PASSWORD
  }
});

const mailListener = new MailListener({
  username: process.env.EMAIL,
  password: process.env.PASSWORD,
  host: "imap.gmail.com",
  port: 993, // imap port
  tls: true,
  connTimeout: 10000, // Default by node-imap
  authTimeout: 5000, // Default by node-imap,
  debug: null, // Or your custom function with only one incoming argument. Default: null
  autotls: 'never', // default by node-imap
  tlsOptions: { rejectUnauthorized: false },
  mailbox: "INBOX", // mailbox to monitor
  searchFilter: ["RECENT"], // Needs to be changed {https://www.npmjs.com/package/node-imap#connection-instance-methods}
  markSeen: true, // all fetched email willbe marked as seen and not fetched next time
  fetchUnreadOnStart: true, // use it only if you want to get all unread email on lib start. Default is `false`,
  attachments: false, // download attachments as they are encountered to the project directory
  attachmentOptions: { directory: "./attachments/" } // specify a download directory for attachments
});

mailListener.start(); // start listening


const  cabs=['ola','uber','rapido'];
const checkValidMail=(subject,attachmentsCount,contentType)=>{
  if(attachmentsCount!=1 && contentType!='application/pdf'){
    return false;
  }
  const sub=subject.toLowerCase().split(' ');
  let subLen=sub.length,cabsLen=cabs.length;
  // for(let i=0;i<subLen;i++){
  //   for(let j=0;j<cabsLen;j++){
  //     if(sub[i]==cabs[j]){
  //       return true;
  //     }
  //   }
  // }
  const c = sub.every(item => cabs.includes(item));
  if(c){
    return true;
  }
  return false;
}
const sendMail=(mailOptions)=>{
  transporter.sendMail(mailOptions, (error, info)=>{
    if (error) {
     console.log(error);
     } else {
     console.log('Email sent: ' + info.response);
     }
   }); 
}
mailListener.on("mail", (mail, seqno)=>{
  const subject=mail.headers.get('subject');
  const mailFrom=mail.headers.get('return-path').text;
  const attachments=mail.attachments;

 if(checkValidMail(subject,attachments[0].length,attachments[0].contentType)){
    const pdf=attachments[0].content;
    const formData = new FormData();
    formData.append('file', pdf, {
      filename: attachments[0].filename,
      contentType: attachments[0].contentType
    });
    axios.post('http://127.0.0.1:5000/extractInvoice/', formData).then((res)=>{
           const url=encodeURI(`http://localhost:5173/?amt=${res.data.amount}&Mode=${res.data.travelMode}&dis=${res.data.Distance}&src=${res.data.sourceAddress}&dest=${res.data.destinationAddress}&Date=${res.data.Date}`);           
           const mailOptions = {
            from: process.env.EMAIL,
            to: mailFrom,
            subject: 'Your Transcript had been processed successfully!',
            text: `Hi\nClick on the following link to proceed\n${url}`
          };
          sendMail(mailOptions);
       }).catch((err)=>console.error(err));

  }else{
    const mailOptions = {
      from: process.env.EMAIL,
      to: mailFrom,
      subject: 'Invalid Email',
      text: 'Hi,\nMake sure email is attached with one invoice of OLA/UBER and the subject needs to contain OLA or UBER for further processing.'
    };
     sendMail(mailOptions);
  }
});
/*sadsad*/