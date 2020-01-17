import React from "react";
import axios from "axios";

import localStorage from "../services/localStorage";

class Wakeparks extends React.Component {
  state = {
    wakeparks: []
  };

  componentDidMount() {
    this.getWakeparks();
  }

  async getWakeparks() {
    const options = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/wakeparks/`,
      methods: "get",
      headers: {
        "Content-Type": "application/json"
      }
    };

    return axios(options)
      .then(res => {
        this.setState({ wakeparks: res.data });
      })
      .catch(err => {
        // console.log(err);
      });
  }

  render() {
    const { wakeparks } = this.state;

    return (
      <div>
        <h3 className="title">Wakeparks</h3>

        <div>
          {localStorage.isPermitted("post:cableparks") && (
            <span>
              <button className="button is-success is-small">Add Wakepark</button>
            </span>
          )}
          {localStorage.isPermitted("delete:cableparks") && (
            <span>
              <button className="button is-danger is-small">Delete Wakepark</button>
            </span>
          )}
          {localStorage.isPermitted("put:cableparks") && (
            <span>
              <button className="button is-warning is-small">Update Wakepark</button>
            </span>
          )}
        </div>
        <ul>
          {wakeparks &&
            wakeparks.map(wakepark => (
              <li key={wakepark.id} data-testid="wakepark-name">
                {wakepark.name}
              </li>
            ))}
        </ul>
      </div>
    );
  }
}

export default Wakeparks;
