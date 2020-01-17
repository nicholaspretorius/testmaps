import auth0 from "auth0-js";

const url =
  window.location.port !== ""
    ? `${window.location.protocol}//${window.location.hostname}:${window.location.port}`
    : `${window.location.protocol}//${window.location.hostname}`;

class Auth {
  // process.env.REACT_APP_AUTH0_DOMAIN,
  // process.env.REACT_APP_API_AUDIENCE,
  // "http://localhost:3007/callback"

  constructor() {
    this.auth0 = new auth0.WebAuth({
      domain: "nicholaspre.eu.auth0.com",
      audience: "testmaps",
      clientID: "Ry0LjeweiLlu0lqHexljlWwJ8hqWJL9j",
      redirectUri: `${url}/callback`,
      responseType: "token",
      scope: "openid profile email"
    });

    console.log("this.auth: ", this.auth0);
  }

  signIn() {
    this.auth0.authorize();
  }

  handleAuthentication() {
    return new Promise((resolve, reject) => {
      this.auth0.parseHash((err, authResult) => {
        if (err) return reject(err);
        if (!authResult || !authResult.accessToken) {
          return reject(err);
        }
        resolve(authResult);
      });
    }).then(authResult => {
      return new Promise((resolve, reject) => {
        this.auth0.client.userInfo(authResult.accessToken, function(err, user) {
          // Now you have the user's information
          if (err) return reject(err);
          resolve({ user, authResult });
        });
      });
    });
  }

  silentAuth() {
    return new Promise((resolve, reject) => {
      this.auth0.checkSession({}, (err, authResult) => {
        if (err) {
          // TODO: How to remove these from tests...?
          // console.log(err);
          return reject(err);
        }
        resolve(authResult);
      });
    }).then(authResult => {
      return new Promise((resolve, reject) => {
        this.auth0.client.userInfo(authResult.accessToken, function(err, user) {
          // Now you have the user's information
          if (err) {
            // console.log(err);
            return reject(err);
          }
          resolve({ user, authResult });
        });
      });
    });
  }

  signOut() {
    this.auth0.logout({
      returnTo: `${url}`,
      clientID: "Ry0LjeweiLlu0lqHexljlWwJ8hqWJL9j"
    });
  }
}

const auth = new Auth();

export default auth;
