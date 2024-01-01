import React from "react";
import styled from "styled-components";
import ReplayOutlinedIcon from "@mui/icons-material/ReplayOutlined";

const StyledNavbar = styled.div`
  background-color: #2e4980;
  width: 100%;
  height: 18vh;
  margin-top: 0vh;
  margin-bottom: 0vh;
  display: flex;

  align-items: center;
`;

const ContainerNav = styled.div`
  width: 100%;
  /* position: absolute; */
`;

const LogoContainer = styled.div`
  display: flex;
  align-items: center;
`;

const Logo = styled.img`
  width: 25vh;
  height: 100px;
  margin-right: 10px;
`;

const LogoHeading = styled.span`
  font-size: 20px;
  font-weight: bold;
  color: #fff;
`;

const NavigationLinks = styled.div`
  width: 100%;
`;

const StyledList = styled.a`
  text-decoration: none;
  color: #fff;
  font-size: 18px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s ease-in-out;

  &:hover {
    color: #f2f2f2;
  }
`;

const Button = styled.button`
  background: -webkit-linear-gradient(left, #003366, #004080, #0059b3, #0073e6);
  height: 10vh;
  width: 10vh;
  color: white;
  font-weight: bold;
  font-size: 1em;
  border-radius: 50%;
  cursor: pointer;
  transition: opacity 0.3s ease-in-out;
  &:hover {
    transform: translateY(-5px);
    color: white;
  }
`;

const Navbar = () => {
  return (
    <StyledNavbar>
      <ContainerNav>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <Logo src="https://firebasestorage.googleapis.com/v0/b/ess-authentication-fb04c.appspot.com/o/pngwing.com%20(3).png?alt=media&token=a2a8ea41-6a36-48db-a519-dc6a1cc0a3c2"></Logo>
          <div
            style={{
              display: "flex",
              justifyContent: "space-around",
              marginRight: "10vh",
            }}
          >
            <Logo
              style={{ cursor: "pointer" }}
              src="https://firebasestorage.googleapis.com/v0/b/ess-authentication-fb04c.appspot.com/o/google-maps-svgrepo-com.svg?alt=media&token=70b1ba0f-e8a8-40d9-b47e-b9b52e5346f7"
            ></Logo>
            <StyledList href="/">
              <div>
                <i style={{ fontSize: "8vh" }} class="fa-solid fa-upload"></i>
                <h4>Upload</h4>
              </div>
            </StyledList>
          </div>
        </div>
      </ContainerNav>
    </StyledNavbar>
  );
};

export default Navbar;
