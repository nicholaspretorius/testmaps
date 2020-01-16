import React from "react";
import axios from "axios";

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
