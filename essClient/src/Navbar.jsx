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

const Navbar = () => {
  return (
    <StyledNavbar>
      <ContainerNav>
        <LogoContainer>
          <Logo src='upload.svg'></Logo>
          <LogoHeading>ESS</LogoHeading>
        </LogoContainer>
        <NavigationLinks>
          <StyledList href="/">Dashboard</StyledList>
        </NavigationLinks>
      </ContainerNav>
    </StyledNavbar>
  );
};

export default Navbar;
