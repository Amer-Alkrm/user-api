import React, { Component } from "react";

// Stateless Functional Component sfc
const NavBar = (props) => {
  return (
    <nav className="navbar navbar-light bg-light">
      <div className="container-fluid">
        <a className="navbar-brand" href="#">
          NavBar
          <span className="badge bg-pill bg-secondary m-2">
            {props.totalCounters}
          </span>
        </a>
      </div>
    </nav>
  );
};

export default NavBar;
