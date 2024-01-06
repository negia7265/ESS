import styled from 'styled-components';
import { nanoid } from 'nanoid'
import { useState } from 'react';

const Type=styled.div`
    color: rgb(19, 19, 19);
    width: 100%;
    border: none;
    background-color: white;
    text-align:center;
`
const Subheading=styled.span`
background-color: white;
font-family: 'Roboto Slab', serif;
font-weight: 700;
font-size: 24px; 
`
const Value=styled.span`
height:40px;
margin: 1px;
border-radius: 3px;
background-color: rgb(190, 195, 214);  
font-weight:bold;
width:100%;
border: none;
cursor: pointer;
font-size: 16px;
padding-left: 6px;
padding-top: 10px;
display:flex;
justify-content:space-between;
transition: opacity 0.3s ease-in-out;
&:hover{
 background: -webkit-linear-gradient(left, #003366,#004080,#0059b3, #0073e6);
 transform: translateY(-5px);
 color:white;
}
`
const ChangeValue=styled.button`
font-size: 18px;
font-weight: 600;
align-items: center;
color: white;
cursor: pointer;
border: none;
min-width:344px;
height:57px;
border-radius: 5px;
background: -webkit-linear-gradient(left, #003366,#004080,#0059b3, #0073e6);
`;
const CandidateDisplay=styled.div`
margin:10px;
margin-bottom: 25px;
border-radius: 10px;
display: flex;
padding: 10px;
text-align:center;
flex-direction: column;
`;
const Field = styled.div`
  height: 50px;
  width: 100%;
  border:0px;
`;

const Input = styled.input`
  height: 100%;
  width: 100%;
  outline: none;
  padding-left: 15px;
  border: 1px solid lightgrey;
  border-bottom-width: 2px;
  font-size: 17px;
  transition: all 0.3s ease;

  &:focus {
    border-color: #1a75ff;
  }

  &::placeholder {
    color: #999;
    transition: all 0.3s ease;
  }

  &:focus::placeholder {
    color: #1a75ff;
  }
`;
const Candidates=({candidateType,predictions})=>{
  const [value,setValue]=useState(predictions.length>0?predictions[0][0]:'');
    return <CandidateDisplay >
            <Type>
              <Subheading>{candidateType}</Subheading>
            </Type>
            <Field>
              <Input type="text" placeholder={candidateType+'...'} value={value} onChange={(e)=>setValue(e.target.value)}  required />
            </Field>
             { predictions.length>0 && predictions.map((prediction) => {
              return <Value key={nanoid()} onClick={()=>setValue(prediction[0])} ><div>{prediction[0]}</div>  <div>{(prediction[1]*100).toFixed(2)}%</div></Value>
              })}          
    </CandidateDisplay>
}

export default Candidates;
