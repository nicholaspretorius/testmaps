import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import auth from "./../services/auth";

class Callback extends Component {
  componentDidMount() {
    auth
      .handleAuthentication()
      .then(() => {
        this.props.history.replace("/");
      })
      .catch(err => {
        console.log(err);
      });
  }

  render() {
    return <p>Loading profile...</p>;
  }
}

export default withRouter(Callback);
