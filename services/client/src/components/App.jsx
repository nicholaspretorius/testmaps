import React from "react";
import { Switch, Route } from "react-router-dom";
import axios from "axios";

import NavBar from "./NavBar";
import Users from "./Users";
import AddUser from "./AddUser";
import About from "./About";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";
import UserStatus from "./UserStatus";

class App extends React.Component {
  state = {
    users: [],
    title: "Testmaps",
    accessToken: null
  };

  getUsers() {
    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users/`)
      .then(res => {
        this.setState({ users: res.data });
      })
      .catch(err => {
        // console.log(err);
      });
  }

  addUser = data => {
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users/`, data)
      .then(res => {
        this.getUsers();
      })
      .catch(err => {
        // console.log(err);
      });
  };

  handleRegisterFormSubmit = data => {
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/register`, data)
      .then(res => {
        console.log("Register: ", res.data);
        this.setState({ accessToken: res.data.access_token });
        this.getUsers();
      })
      .catch(err => {
        console.log(err);
      });
  };

  handleLoginFormSubmit = data => {
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/login`, data)
      .then(res => {
        console.log("Login: ", res.data);
        this.setState({ accessToken: res.data.access_token });
        this.getUsers();
        window.localStorage.setItem("refreshToken", res.data.refresh_token);
      })
      .catch(err => {
        console.log(err);
      });
  };

  validRefresh = () => {
    const token = window.localStorage.getItem("refreshToken");

    if (token) {
      axios
        .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/refresh`, {
          refresh_token: token
        })
        .then(res => {
          this.setState({ accessToken: res.data.access_token });
          this.getUsers();
          window.localStorage.setItem("refreshToken", res.data.refresh_token);
          return true;
        })
        .catch(err => {
          console.log(err);
          return false;
        });
    }
    return false;
  };

  isAuthenticated = () => {
    if (this.state.accessToken || this.validRefresh()) {
      return true;
    }
    return false;
  };

  logoutUser = () => {
    window.localStorage.removeItem("refreshToken");
    this.setState({ accessToken: null });
    console.log("Logout...");
  };

  componentDidMount() {
    this.getUsers();
  }

  render() {
    const { title, accessToken } = this.state;

    return (
      <div>
        <NavBar
          title={title}
          logoutUser={this.logoutUser}
          isAuthenticated={this.isAuthenticated}
        />
        <section className="section">
          <div className="container">
            <div className="columns">
              <div className="column is-one-third">
                <br />
                <Switch>
                  <Route
                    path="/login"
                    render={() => (
                      <LoginForm
                        onHandleLoginFormSubmit={this.handleLoginFormSubmit}
                        isAuthenticated={this.isAuthenticated}
                      />
                    )}
                  />
                  <Route
                    path="/register"
                    render={() => (
                      <RegisterForm
                        onHandleRegisterFormSubmit={
                          this.handleRegisterFormSubmit
                        }
                        isAuthenticated={this.isAuthenticated}
                      />
                    )}
                  />
                  <Route
                    exact
                    path="/status"
                    render={() => (
                      <UserStatus
                        accessToken={accessToken}
                        isAuthenticated={this.isAuthenticated}
                      />
                    )}
                  />
                  <Route
                    exact
                    path="/"
                    render={() => (
                      <div>
                        <h1 className="title is-1 is-1">Users</h1>
                        <hr />
                        <br />
                        <AddUser addUser={this.addUser} />
                        <hr />
                        <br />
                        <Users users={this.state.users} />
                      </div>
                    )}
                  />
                  <Route exact path="/about" component={About} />
                </Switch>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default App;
