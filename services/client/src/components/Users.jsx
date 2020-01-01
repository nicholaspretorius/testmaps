import React from "react";

const Users = props => {
  const { users } = props;

  return (
    <div>
      {users.map(user => (
        <p key={user.id} className="box title is-4 username">
          {user.email}
        </p>
      ))}
    </div>
  );
};

export default Users;
