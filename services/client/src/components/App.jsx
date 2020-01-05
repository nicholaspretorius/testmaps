import React from "react";
import axios from "axios";

import Users from "./Users";
import AddUser from "./AddUser";

class App extends React.Component {
  state = {
    users: [],
    email: ""
  };

  getUsers() {
    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users/`)
      .then(res => {
        this.setState({ users: res.data });
      })
      .catch(err => {
        console.log(err);
      });
  }

  addUser = event => {
    event.preventDefault();

    const data = {
      email: this.state.email
    };

    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users/`, data)
      .then(res => {
        this.getUsers();
        this.setState({ email: "" });
      })
      .catch(err => {
        console.log(err);
      });
  };

  handleChange = event => {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };

  componentDidMount() {
    this.getUsers();
  }

  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-one-third">
              <br />
              <h1 className="title is-1 is-1">Users</h1>
              <hr />
              <br />
              <AddUser
                addUser={this.addUser}
                email={this.state.email}
                onHandleChange={this.handleChange}
              />
              <hr />
              <br />
              <Users users={this.state.users} />
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default App;
