import React from "react";
import PropTypes from "prop-types";

const Users = props => {
  const { users, removeUser, isAuthenticated } = props;

  return (
    <div>
      <table className="table is-hoverable is-fullwidth">
        <thead>
          <tr>
            <th>Id</th>
            <th>Email</th>
            {isAuthenticated() && <th />}
          </tr>
        </thead>
        <tbody>
          {users.map(user => {
            return (
              <tr key={user.email}>
                <td>{user.id}</td>
                <td className="user-email">{user.email}</td>
                {isAuthenticated() && (
                  <td>
                    <button
                      className="button is-danger is-small"
                      onClick={() => removeUser(user.id)}
                    >
                      Delete
                    </button>
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

Users.propTypes = {
  users: PropTypes.array.isRequired,
  removeUser: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired
};

export default Users;
