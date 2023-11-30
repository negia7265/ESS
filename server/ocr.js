const sharp = require('sharp');
const { createWorker} = require('tesseract.js');

const preprocess_img=(invoice_image)=>{
  return  sharp(invoice_image).greyscale().threshold().toBuffer()
}

const OCR=async (invoice_image)=>{
    const worker = await createWorker('eng');
    const ret = await worker.recognize(invoice_image);
    await worker.terminate();  
    return {'tsv':ret.data.tsv,'text':ret.data.text}
}
module.exports=OCR
