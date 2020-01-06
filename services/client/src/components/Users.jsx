import React from "react";
import PropTypes from "prop-types";

const Users = props => {
  const { users } = props;

  return (
    <div>
      <table className="table is-hoverable is-fullwidth">
        <thead>
          <tr>
            <th>Id</th>
            <th>Email</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {users.map(user => {
            return (
              <tr key={user.email}>
                <td>{user.id}</td>
                <td className="user-email">{user.email}</td>
                <td>
                  <button className="button is-danger is-small">Delete</button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

Users.propTypes = {
  users: PropTypes.array.isRequired
};

export default Users;
