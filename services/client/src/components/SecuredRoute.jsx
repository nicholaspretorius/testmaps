import React from "react";
import { Route } from "react-router-dom";

function SecuredRoute(props) {
  // isAuth, signIn
  const { render: Component, path } = props;
  return (
    <Route
      path={path}
      render={() => {
        // if (!isAuth()) {
        //   signIn();
        //   return <div></div>;
        // }
        return <Component />;
      }}
    />
  );
}

export default SecuredRoute;
