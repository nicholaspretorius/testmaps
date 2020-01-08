import React from "react";
import { Route } from "react-router-dom";
import auth from "./../services/auth";

function SecuredRoute(props) {
  const { component: Component, path } = props;
  return (
    <Route
      path={path}
      render={() => {
        if (!auth.isAuthenticated()) {
          auth.signIn();
          return <div></div>;
        }
        return <Component />;
      }}
    />
  );
}

export default SecuredRoute;
