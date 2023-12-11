import { useState, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`; 

function MyApp() {
  const [numPages, setNumPages] = useState();
  const [pageNumber, setPageNumber] = useState(1);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages)
  }

  const goToPreviousPage = () => {
    if (pageNumber > 1) {
      setPageNumber(pageNumber - 1);
    }
  };

  const goToNextPage = () => {
    const totalNumberOfPages = 10;
    if (pageNumber < totalNumberOfPages) {
      setPageNumber(pageNumber + 1);
    }
  };


  return (
    <div>
      <Document file="../OLA_1.pdf" onLoadSuccess={onDocumentLoadSuccess}>
        
      <div className="page-controls">
        <button
          disabled={pageNumber <= 1}
          onClick={() => setPageNumber(pageNumber - 1)}
          type="button"
          aria-label="Previous page"
        >
          ‹
        </button>
        <span>
          {pageNumber}
          {' '}
          of
          {' '}
          {numPages}
        </span>
        <button
          disabled={pageNumber >= numPages}
          onClick={() => setPageNumber(pageNumber + 1)}
          type="button"
          aria-label="Next page"
        >
          ›
        </button>
      </div>
        <Page pageNumber={pageNumber} />
      </Document>
      <p>
        Page {pageNumber} of {numPages}
      </p>
    </div>
  );
}

export default MyApp;

