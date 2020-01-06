import React from "react";
import { Switch, Route } from "react-router-dom";
import axios from "axios";

import NavBar from "./NavBar";
import Users from "./Users";
import AddUser from "./AddUser";
import About from "./About";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

class App extends React.Component {
  state = {
    users: [],
    title: "Testmaps"
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
      })
      .catch(err => {
        console.log(err);
      });
  };

  componentDidMount() {
    this.getUsers();
  }

  render() {
    const { title } = this.state;

    return (
      <div>
        <NavBar title={title} />
        <section className="section">
          <div className="container">
            <div className="columns">
              <div className="column is-one-third">
                <br />
                <Switch>
                  <Route
                    path="/login"
                    render={() => <LoginForm handleLoginFormSubmit={this.handleLoginFormSubmit} />}
                  />
                  <Route
                    path="/register"
                    render={() => (
                      <RegisterForm handleRegisterFormSubmit={this.handleRegisterFormSubmit} />
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
