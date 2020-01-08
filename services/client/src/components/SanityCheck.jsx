import React, { Component } from "react";
import axios from "axios";

import auth0Client from "./Auth0";

class SanityCheck extends Component {
  state = {
    message: "",
    profile: null
  };

  componentDidMount() {
    this.getSanityCheck();
    const profile = auth0Client.getProfile();
    console.log("Profile: ", profile);
    this.setState({ profile });
  }

  async getSanityCheck() {
    const options = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/sanity/`,
      methods: "get",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${auth0Client.getAccessToken()}`
      }
    };

    try {
      const res = await axios(options);
      console.log("Res: ", res);
    } catch (err) {
      console.log("Error: ", err);
    }
  }

  render() {
    return (
      <div>
        <h3>Sanity Check</h3>
        <div></div>
      </div>
    );
  }
}

export default SanityCheck;
