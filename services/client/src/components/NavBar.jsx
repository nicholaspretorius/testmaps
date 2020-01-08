import React from "react";
import { Link, withRouter } from "react-router-dom";
import PropTypes from "prop-types";

import auth from "./../services/auth";
import "./NavBar.css";

const titleStyle = {
  fontWeight: "bold"
};

const NavBar = props => {
  const { title, logoutUser, isAuthenticated } = props;

  const signOutAuth0 = () => {
    auth.signOut();
    props.history.replace("/");
  };

  let menu = (
    <div className="navbar-menu">
      <div className="navbar-start">
        <Link to="/about" className="navbar-item" data-testid="nav-about">
          About
        </Link>
      </div>
      <div className="navbar-end">
        <Link to="/register" className="navbar-item" data-testid="nav-register">
          Register
        </Link>
        <Link to="/login" className="navbar-item" data-testid="nav-login">
          Login
        </Link>
        {!auth.isAuthenticated() && (
          // eslint-disable-next-line react/jsx-handler-names
          <span className="navbar-item link" onClick={auth.signIn}>
            Auth0 Sign In
          </span>
        )}
        {auth.isAuthenticated() && (
          <>
            <div className="navbar-item">{auth.getProfile().name}</div>

            <div
              className="navbar-item link"
              onClick={() => {
                signOutAuth0();
              }}
            >
              Auth0 Sign Out
            </div>
          </>
        )}
      </div>
    </div>
  );
  if (isAuthenticated()) {
    menu = (
      <div className="navbar-menu">
        <div className="navbar-start">
          <Link to="/about" className="navbar-item" data-testid="nav-about">
            About
          </Link>
          <Link to="/status" className="navbar-item" data-testid="nav-status">
            User Status
          </Link>
        </div>
        <div className="navbar-end">
          <span onClick={logoutUser} className="navbar-item link" data-testid="nav-logout">
            Logout
          </span>
        </div>
      </div>
    );
  }

  return (
    <nav className="navbar is-dark" role="navigation" aria-label="main navigation">
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
  logoutUser: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired
};

export default withRouter(NavBar);
