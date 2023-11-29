const sharp = require('sharp');
const { createScheduler, createWorker} = require('tesseract.js');

//get number of cpu cores for OCR parralel processing 
const os = require('os');
const cpus = os.cpus();
const numberOfCores = cpus.length;

const preprocess_img=(image)=>{
  return  sharp(image).greyscale().threshold().toBuffer()
}

//parralel processing of images
const OCR=async (files)=> {
  const scheduler = createScheduler();

  // Creates workers and adds to scheduler
  const workerGen = async () => {
    const worker = await createWorker("eng", 1, { cachePath: "." });
    scheduler.addWorker(worker);
  };

  //Build each tesseract worker for  cpu cores
  const workerPromises = Array(numberOfCores).fill(null).map(workerGen);
  await Promise.all(workerPromises);
  
  const data={
    'pdf':[],
    'page':[]
  }
  for(let i=0;i<files.length;i++){
    if(files[i].mimetype=='application/pdf'){
      
    }else{
      data.page.push(scheduler.addJob('recognize', files[i].buffer).then((x) =>{
     
      }));  
    }
  }
  data.page= await Promise.all(
    files.map((file) =>{
      console.log('got here')
      if(file.mimetype=='application/pdf'){
        console.log('pdf here ')
         data.pdf.push(file)
      }else {
         scheduler.addJob('recognize', file.buffer).then((result) => ({
          'tsv':result.data.tsv,
          'text':result.data.text
        }))    
      }
    })
  );
  // It also terminates all workers.
  await scheduler.terminate();   
  return data;
}

module.exports=OCR
