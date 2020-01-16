import React from "react";
import { Link, withRouter } from "react-router-dom";
import PropTypes from "prop-types";

import "./NavBar.css";

const titleStyle = {
  fontWeight: "bold"
};

const NavBar = props => {
  // logoutUser, isAuthenticated
  const { title, signIn, signOut, profile, isAuth } = props;

  let menu = (
    <div className="navbar-menu">
      <div className="navbar-start">
        <Link to="/about" className="navbar-item" data-testid="nav-about">
          About
        </Link>
        {isAuth() && (
          <>
            <Link
              to="/profile"
              className="navbar-item"
              data-testid="nav-profile"
            >
              Profile
            </Link>
            <Link to="/sanity" className="navbar-item" data-testid="nav-sanity">
              Sanity
            </Link>
          </>
        )}
      </div>
      <div className="navbar-end">
        {/* <Link to="/register" className="navbar-item" data-testid="nav-register">
          Register
        </Link>
        <Link to="/login" className="navbar-item" data-testid="nav-login">
          Login
        </Link> */}
        {isAuth() && (
          <>
            <div className="navbar-item">{profile.name}</div>

            <div
              className="navbar-item link"
              onClick={signOut}
              data-testid="nav-signout"
            >
              SignOut
            </div>
          </>
        )}

        {!isAuth() && (
          <span
            className="navbar-item link"
            onClick={signIn}
            data-testid="nav-signin"
          >
            SignIn
          </span>
        )}
      </div>
    </div>
  );
  // if (isAuthenticated()) {
  //   menu = (
  //     <div className="navbar-menu">
  //       <div className="navbar-start">
  //         <Link to="/about" className="navbar-item" data-testid="nav-about">
  //           About
  //         </Link>
  //         <Link to="/status" className="navbar-item" data-testid="nav-status">
  //           User Status
  //         </Link>
  //       </div>
  //       <div className="navbar-end">
  //         <span onClick={logoutUser} className="navbar-item link" data-testid="nav-logout">
  //           Logout
  //         </span>
  //       </div>
  //     </div>
  //   );
  // }

  return (
    <nav
      className="navbar is-dark"
      role="navigation"
      aria-label="main navigation"
    >
      <section className="container">
        <div className="navbar-brand">
          <Link to="/" className="navbar-item nav-title" style={titleStyle}>
            {title}
          </Link>
          <span
            className="nav-toggle navbar-burger"
            onClick={() => {
              let toggle = document.querySelector(".nav-toggle");
              let menu = document.querySelector(".navbar-menu");
              toggle.classList.toggle("is-active");
              menu.classList.toggle("is-active");
            }}
          >
            <span />
            <span />
            <span />
          </span>
        </div>
        {menu}
      </section>
    </nav>
  );
};

NavBar.propTypes = {
  title: PropTypes.string.isRequired,
  isAuth: PropTypes.func.isRequired,
  signIn: PropTypes.func.isRequired,
  signOut: PropTypes.func.isRequired
  // logoutUser: PropTypes.func.isRequired,
  // isAuthenticated: PropTypes.func.isRequired
};

export default withRouter(NavBar);
