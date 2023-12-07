import React from 'react';
import styled from 'styled-components';

const StyledNavbar = styled.div`
  background-color: #3498db;
  width:100%;
  height:7vh;
  justify-content: space-between;
  align-items: center;
`;

const ContainerNav = styled.div`
  display: flex;
  align-items: center;
  width:100%;
  position:absolute
`;

const LogoContainer = styled.div`
  display: flex;
  align-items: center;
`;

const Logo = styled.img`
  width: 50px;
  height: 50px;
  margin-right: 10px;
`;

const LogoHeading = styled.span`
  font-size: 20px;
  font-weight: bold;
  color: #fff;
`;

const NavigationLinks = styled.div`
  display: flex;
  justify-content: flex-end;
  width:100%;
  align-items: center;
`;

const StyledList = styled.a`
  text-decoration: none;
  color: #fff;
  margin-right: 20px;
  font-size: 18px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s ease-in-out;

  &:hover {
    color: #f2f2f2;
  }
`;

const Button = styled.button`
  background: -webkit-linear-gradient(left, #003366,#004080,#0059b3, #0073e6);
  height:2.3em;
  width:13em;
  color:white;
  font-weight:bold;
  font-size:1em;
  border-radius:1em;
  cursor:pointer;
  transition: opacity 0.3s ease-in-out;
  &:hover{
  transform: translateY(-5px);
  color:white;
  }
`;

const Navbar = () => {
  return (
    <StyledNavbar>
      <ContainerNav>
        <LogoContainer>
          <Logo src='upload.svg'></Logo>
          <LogoHeading>ESS</LogoHeading>
        </LogoContainer>
        <NavigationLinks>
          <StyledList href="/">
            <Button>
              Automate Invoice Upload 
            </Button>
            </StyledList>
        </NavigationLinks>
      </ContainerNav>
    </StyledNavbar>
  );
};

export default Navbar;
