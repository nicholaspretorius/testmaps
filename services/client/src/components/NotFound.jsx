import React from "react";
import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div>
      <h3 className="title">404 Not Found.</h3>
      <div>
        <p data-testid="not-found">
          Unfortunately there is no page with that url.
        </p>
        <Link to="/">Home</Link>
      </div>
    </div>
  );
};

export default NotFound;
