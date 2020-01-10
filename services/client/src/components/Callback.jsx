import React, { Component } from "react";
import { withRouter } from "react-router-dom";
// import auth from "./../services/auth";

class Callback extends Component {
  componentDidMount() {
    this.props.onHandleAuth();
  }

  render() {
    return <p>Loading profile...</p>;
  }
}

export default withRouter(Callback);
