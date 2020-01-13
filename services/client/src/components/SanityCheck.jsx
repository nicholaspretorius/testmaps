import React, { Component } from "react";
import axios from "axios";

import localStorage from "./../services/localStorage";

class SanityCheck extends Component {
  state = {
    message: ""
  };

  componentDidMount() {
    this.getSanityCheck();
  }

  getSanityCheck() {
    const options = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/sanity/`,
      methods: "get",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`
      }
    };

    return axios(options)
      .then(res => {
        this.setState({ message: res.data.hello });
      })
      .catch(err => {
        console.log("Error: ", err);
      });
  }

  render() {
    const { message } = this.state;

    return (
      <div>
        <h3>Sanity Check</h3>
        <div data-testid="message">{message}</div>
      </div>
    );
  }
}

export default SanityCheck;
