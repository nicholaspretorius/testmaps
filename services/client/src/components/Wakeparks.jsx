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
              <button className="button is-success is-small">
                Add Wakepark
              </button>
            </span>
          )}
        </div>

        <table className="table is-hoverable is-fullwidth">
          <thead>
            <tr>
              <th>Name</th>
              <th>Location</th>
              <th>Instagram</th>
              <th>{localStorage.isPermitted("put:cableparks") && "Edit"}</th>
              <th>
                {localStorage.isPermitted("delete:cableparks") && "Delete"}
              </th>
            </tr>
          </thead>
          <tbody>
            {wakeparks &&
              wakeparks.map(wakepark => (
                <tr key={wakepark.id} data-testid="wakepark-name">
                  <td>{wakepark.name}</td>
                  {wakepark.location && (
                    <td>
                      Lat: {wakepark.location.lat}, Lng: {wakepark.location.lng}
                    </td>
                  )}
                  {wakepark.social && <td>{wakepark.social.instagram}</td>}
                  <td>
                    {localStorage.isPermitted("put:cableparks") && (
                      <button className="button is-warning is-small">
                        Update Wakepark
                      </button>
                    )}
                  </td>
                  <td>
                    {localStorage.isPermitted("delete:cableparks") && (
                      <button className="button is-danger is-small">
                        Delete Wakepark
                      </button>
                    )}
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    );
  }
}

export default Wakeparks;
