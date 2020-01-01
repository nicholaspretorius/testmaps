import React from "react";
import PropTypes from "prop-types";

const AddUser = props => {
  const { addUser, email, handleChange } = props;

  return (
    <form onSubmit={e => addUser(e)}>
      <div className="field">
        <label htmlFor="input-email" className="label is-large">
          Email
        </label>
        <input
          type="email"
          name="email"
          id="input-email"
          className="input is-large"
          placeholder="Enter your email address"
          value={email}
          onChange={handleChange}
          required
        ></input>
      </div>
      <input type="submit" className="button is-primary is-large is-fullwidth" value="Submit" />
    </form>
  );
};

AddUser.propTypes = {
  email: PropTypes.string.isRequired,
  handleChange: PropTypes.func.isRequired,
  addUser: PropTypes.func.isRequired
};

export default AddUser;