import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import auth0Client from "./Auth0";

class Callback extends Component {
  componentDidMount() {
    auth0Client
      .handleAuthentication()
      .then(res => {
        console.log("Auth0ing...");
        this.props.history.replace("/");
      })
      .catch(err => {
        console.log("Auth0", err);
      });
  }

  render() {
    return <p>Loading profile...</p>;
  }
}

export default withRouter(Callback);
