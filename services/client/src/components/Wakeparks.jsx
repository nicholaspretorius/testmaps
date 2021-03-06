import React from "react";
import { Link } from "react-router-dom";
import axios from "axios";

import localStorage from "./../services/localStorage";
import isPermittedAndOwner from "./../services/can";

class Wakeparks extends React.Component {
  state = {
    wakeparks: [],
    isLoading: true
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
        this.setState({ wakeparks: res.data, isLoading: false });
      })
      .catch(err => {
        // console.log(err);
      });
  }

  async deleteWakepark(id) {
    const res = this.props.deleteWakepark(id);
    const wakeparks_existing = this.state.wakeparks;
    const wakeparks_updated = this.state.wakeparks.filter(
      wakepark => wakepark.id !== id
    );

    if (res) {
      this.setState({ wakeparks: wakeparks_updated });
    } else {
      this.setState({ wakeparks: wakeparks_existing });
    }
  }

  render() {
    const { wakeparks, isLoading } = this.state;
    const { ownerId } = this.props;

    if (isLoading) {
      return <div>Loading...</div>;
    }

    return (
      <div>
        <h3 className="title">Wakeparks</h3>

        <div className="content">
          {localStorage.isPermitted("post:cableparks") && (
            <span>
              <Link
                to="/add-wakepark"
                className="button is-success is-small"
                data-testid="add-wakepark"
              >
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
                    {isPermittedAndOwner(
                      "put:cableparks",
                      ownerId,
                      wakepark.owner_id
                    ) && (
                      <Link
                        to={`/update-wakepark/${wakepark.id}`}
                        className="button is-warning is-small"
                      >
                        Update Wakepark
                      </Link>
                    )}
                  </td>
                  <td>
                    {isPermittedAndOwner(
                      "delete:cableparks",
                      ownerId,
                      wakepark.owner_id
                    ) && (
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
