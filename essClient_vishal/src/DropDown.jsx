import { useState } from "react";
import styled from "styled-components";
import { ArrowDropDown } from "@mui/icons-material";

const DropdownContainer = styled.div`
  width: 100%;
  user-select: none;
  border:1px solid skyblue;
  position: relative;
`;

const DropdownBtn = styled.div`
  padding: 15px 20px;
  background: #fff;
  box-shadow: 3px 3px 10px 6px rgba(0, 0, 0, 0.06);
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  cursor: pointer;
  justify-content: space-between;
`;

const DropdownContent = styled.div`
  position: absolute;
  z-index:10;
  max-height:15em;
  overflow-y:scroll;
  top: 110%;
  left: 0;
  padding: 10px;
  background: #fff;
  box-shadow: 3px 3px 10px 6px rgba(0, 0, 0, 0.06);
  font-weight: 500;
  color: #333;
  width: 100%;
  background-color:white;

`;

const DropdownItem = styled.div`
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: #f4f4f4;
  }
`;
const Input=styled.input`
  background-color:rgba(0,0,0,0.02);
  width:100%;
  font-size:1.2em;
  height:2em;
`;
function Dropdown({ selected, setSelected,options }) {
  const [isActive, setIsActive] = useState(false);
  return (
    <DropdownContainer>
      <DropdownBtn onClick={() => setIsActive(!isActive)}>
        <Input
          value={selected}
          onChange={(e) => {
            setSelected(e.target.value);
            setIsActive(true);
          }}
        />
        <span > <ArrowDropDown/></span>
      </DropdownBtn>

      {isActive && options.length>0 && (
        <DropdownContent>
          {options.map((option) => {
              return (
                <DropdownItem
                  onClick={() => {
                    setSelected(option);
                    setIsActive(false);
                  }}
                >
                  {option}
                </DropdownItem>
              );
          })}
        </DropdownContent>
      )}
    </DropdownContainer>
  );
}

export default Dropdown;