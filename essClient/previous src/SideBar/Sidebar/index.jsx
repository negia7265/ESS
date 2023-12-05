import React, { useState } from "react";

import {
  Children,
  SidebarContainer,
  SidebarWrapper,
  SidebarLogoWrapper,
  SidebarLogo,
  SidebarBrand,
  SidebarToggler,
} from "./SidebarStyles";
import BrandLogo from "./BrandLogo.svg";

import { SidebarItems } from "..";

const MOBILE_VIEW = window.innerWidth < 468;

export default function Sidebar({ children }) {
  const [displaySidebar, setDisplaySidebar] = useState(!MOBILE_VIEW);

  const handleSidebarDisplay = (e) => {
    e.preventDefault();
    if (window.innerWidth > 468) {
      setDisplaySidebar(!displaySidebar);
    } else {
      setDisplaySidebar(false);
    }
  };

  return (
    <>
    <nav>
        <div className="container-nav">
          <div className="logo1">
            <img className="logo" src={BrandLogo} alt="Brand logo" />
            <span className="logo_heading">ESS</span>
          </div>
          <a href="/Dashboard" className="List">
            DashBoard
          </a>
          <a href="/SignUp" className="List">
            Sign Up
          </a>
          <a href="/Login" className="List">
            Sign In
          </a>
          <a href="#" className="List">
            Sign Out
          </a>
        </div>
      </nav>
      </>
  );
}
