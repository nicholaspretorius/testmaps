import React from "react";
import PropTypes from "prop-types";

const Users = props => {
  const { users } = props;

  return (
    <div>
      {users.map(user => (
        <p key={user.id} className="box title is-4 user-email">
          {user.email}
        </p>
      ))}
    </div>
  );
};

Users.propTypes = {
  users: PropTypes.array.isRequired
};

export default Users;
