import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";

class App extends React.Component {
  state = {
    users: []
  };

  getUsers() {
    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => {
        this.setState({ users: res.data });
      })
      .catch(err => {
        console.log(err);
      });
  }

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
              {this.state.users.map(user => (
                <p key={user.id} className="box title is-4 username">
                  {user.email}
                </p>
              ))}
            </div>
          </div>
        </div>
      </section>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));
