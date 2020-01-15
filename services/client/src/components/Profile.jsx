import React from "react";
import localStorage from "../services/localStorage";
import PropTypes from "prop-types";

const Profile = props => {
  const { profile } = props;
  const accessToken = localStorage.getItem("accessToken") || "";
  return (
    <div className="container is-full columns is-multiline">
      <h3 className="title">Profile</h3>

      {profile && (
        <div className="column user-profile is-full">
          <ul>
            <li>
              Name: <span data-testid="user-name">{profile.name}</span>
            </li>
            <li>
              Email: <span data-testid="user-email">{profile.email}</span>
            </li>
            <li>
              Sub: <span data-testid="user-sub">{profile.sub}</span>
            </li>
          </ul>
        </div>
      )}
      <div className="column access-token is-full">
        Access Token:
        <br />
        <span data-testid="access-token">{accessToken}</span>
      </div>
    </div>
  );
};

Profile.propTypes = {
  profile: PropTypes.object.isRequired
};

export default Profile;
