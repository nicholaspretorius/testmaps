import React from "react";
import { Switch, Route } from "react-router-dom";
import axios from "axios";
import Modal from "react-modal";

import NavBar from "./NavBar";
import AddUser from "./AddUser";
import Users from "./Users";
import About from "./About";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";
import UserStatus from "./UserStatus";
import Message from "./Message";

Modal.setAppElement(document.getElementById("root"));

const modalStyles = {
  content: {
    top: "0",
    left: "0",
    right: "0",
    bottom: "0",
    border: 0,
    background: "transparent"
  }
};

class App extends React.Component {
  state = {
    users: [],
    title: "Testmaps",
    accessToken: null,
    messageType: null,
    messageText: null,
    showModal: false
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
        this.handleCloseModal();
        this.createMessage("success", "User added.");
      })
      .catch(err => {
        // console.log(err);
        this.handleCloseModal();
        this.createMessage("danger", "That user already exists.");
      });
  };

  removeUser = user_id => {
    axios
      .delete(`${process.env.REACT_APP_USERS_SERVICE_URL}/users/${user_id}`)
      .then(res => {
        this.getUsers();
        this.createMessage("success", "User removed.");
      })
      .catch(err => {
        console.log(err);
        this.createMessage("danger", "Something went wrong.");
      });
  };

  handleRegisterFormSubmit = data => {
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/register`, data)
      .then(res => {
        console.log("Register: ", res.data);
        this.createMessage("success", "You have successfully registered.");
        this.setState({ accessToken: res.data.access_token });
        this.getUsers();
      })
      .catch(err => {
        console.log(err);
        this.createMessage("danger", "That user already exists.");
      });
  };

  handleLoginFormSubmit = data => {
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/login`, data)
      .then(res => {
        console.log("Login: ", res.data);
        this.setState({ accessToken: res.data.access_token });
        this.createMessage("success", "You have logged in successfully.");
        this.getUsers();
        window.localStorage.setItem("refreshToken", res.data.refresh_token);
      })
      .catch(err => {
        console.log(err);
        this.createMessage("danger", "Incorrect email and/or password.");
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
    this.createMessage("success", "You have logged out.");
  };

  createMessage = (type, text) => {
    this.setState({
      messageType: type,
      messageText: text
    });

    // removeMessage after 3 seconds
    setTimeout(() => {
      this.removeMessage();
    }, 3000);
  };

  removeMessage = () => {
    this.setState({
      messageType: null,
      messageText: null
    });
  };

  handleOpenModal = () => {
    this.setState({ showModal: true });
  };

  handleCloseModal = () => {
    this.setState({ showModal: false });
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
            {this.state.messageType && this.state.messageText && (
              <Message
                messageType={this.state.messageType}
                messageText={this.state.messageText}
                removeMessage={this.removeMessage}
              />
            )}
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
                        {this.isAuthenticated() && (
                          <button
                            onClick={this.handleOpenModal}
                            className="button is-primary"
                          >
                            Add User
                          </button>
                        )}
                        <br />
                        <br />
                        <Modal
                          isOpen={this.state.showModal}
                          style={modalStyles}
                        >
                          <div className="modal is-active">
                            <div className="modal-background" />
                            <div className="modal-card">
                              <header className="modal-card-head">
                                <p className="modal-card-title">Add User</p>
                                <button
                                  className="delete"
                                  aria-label="close"
                                  onClick={this.handleCloseModal}
                                />
                              </header>
                              <section className="modal-card-body">
                                <AddUser addUser={this.addUser} />
                              </section>
                            </div>
                          </div>
                        </Modal>
                        <Users
                          users={this.state.users}
                          removeUser={this.removeUser}
                          isAuthenticated={this.isAuthenticated}
                        />
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
