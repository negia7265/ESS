import Styled from 'styled-components';
const FileUploadCounter=()=>{
    const Circle=Styled.div`
    background-color: #94ff6f;
    border-radius: 50%;
    height: 71px;
    width: 74px;
    color: #ff1c1c;
    font-family: "Itim-Regular", Helvetica;
    font-size: 50px;
    font-weight: 400;
    text-align:center;
    line-height: normal;
    position: fixed;
    text-shadow: 0px 4px 4px #00000040;
    `;
    return <>
     <img src='/upload' alt='upload svg'/>
     <Circle>
            3
     </Circle>
    </>
}

export default FileUploadCounter;