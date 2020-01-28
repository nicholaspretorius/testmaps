import React from "react";

import Wakeparks from "./Wakeparks";

const Home = props => {
  return (
    <Wakeparks deleteWakepark={props.deleteWakepark} ownerId={props.ownerId} />
  );
};

export default Home;
