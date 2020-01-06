import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import PropTypes from "prop-types";
import axios from "axios";

class UserStatus extends Component {
  state = {
    id: null,
    email: ""
  };

  componentDidMount() {
    this.getUserStatus();
  }

  getUserStatus() {
    const options = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`,
      methods: "get",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.props.accessToken}`
      }
    };

    return axios(options)
      .then(res => {
        this.setState({
          id: res.data.id,
          email: res.data.email
        });
      })
      .catch(err => {
        console.log(err);
      });
  }

  render() {
    const { id, email } = this.state;
    const { isAuthenticated } = this.props;

    if (!isAuthenticated()) {
      return <Redirect to="/login" />;
    }

    return (
      <div>
        <ul>
          <li>
            <strong>Id:</strong> <span data-testid="user-id">{id}</span>
          </li>
          <li>
            <strong>Email:</strong>{" "}
            <span data-testid="user-email">{email}</span>
          </li>
        </ul>
      </div>
    );
  }
}

UserStatus.propTypes = {
  accessToken: PropTypes.string,
  isAuthenticated: PropTypes.func.isRequired
};

export default UserStatus;
