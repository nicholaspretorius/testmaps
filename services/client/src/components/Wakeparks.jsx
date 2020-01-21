import React from "react";
import { Link } from "react-router-dom";
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

  async deleteWakepark(id) {
    const options = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/wakeparks/${id}`,
      method: "delete",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`
      }
    };

    try {
      const res = await axios(options);
      if (res.status === 200) {
        this.getWakeparks();
      }
    } catch (ex) {}
  }

  render() {
    const { wakeparks } = this.state;

    return (
      <div>
        <h3 className="title">Wakeparks</h3>

        <div className="content">
          {localStorage.isPermitted("post:cableparks") && (
            <span>
              <Link to="/add-wakepark" className="button is-success is-small">
                Add Wakepark
              </Link>
            </span>
          )}
        </div>
        {wakeparks && wakeparks.length === 0 && (
          <div className="content">
            <p>Unfortunately, there are currently no wakeparks listed.</p>
          </div>
        )}
        {wakeparks && wakeparks.length > 0 && (
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
              {wakeparks.map(wakepark => (
                <tr key={wakepark.id}>
                  <td data-testid="wakepark-name">{wakepark.name}</td>
                  {wakepark.location && (
                    <td>
                      Lat: {wakepark.location.lat}, Lng: {wakepark.location.lng}
                    </td>
                  )}
                  {wakepark.social && <td>{wakepark.social.instagram}</td>}
                  <td>
                    {localStorage.isPermitted("put:cableparks") && (
                      <Link
                        to={`/update-wakepark/${wakepark.id}`}
                        className="button is-warning is-small"
                      >
                        Update Wakepark
                      </Link>
                    )}
                  </td>
                  <td>
                    {localStorage.isPermitted("delete:cableparks") && (
                      <button
                        className="button is-danger is-small"
                        onClick={() => this.deleteWakepark(wakepark.id)}
                      >
                        Delete Wakepark
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    );
  }
}

export default Wakeparks;
