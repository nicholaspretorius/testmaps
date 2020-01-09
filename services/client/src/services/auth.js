import auth0 from "auth0-js";

class Auth {
  constructor() {
    this.auth0 = new auth0.WebAuth({
      domain: process.env.REACT_APP_AUTH0_DOMAIN,
      audience: process.env.REACT_APP_API_AUDIENCE,
      clientID: process.env.REACT_APP_AUTH0_CLIENT_ID,
      redirectUri: "http://localhost:3007/callback",
      responseType: "token",
      scope: "openid profile email"
    });

    this.handleAuthentication = this.handleAuthentication.bind(this);
    this.getProfile = this.getProfile.bind(this);
    this.isAuthenticated = this.isAuthenticated.bind(this);
    this.signIn = this.signIn.bind(this);
    this.signOut = this.signOut.bind(this);
  }

  getProfile() {
    return this.profile;
  }

  getIdToken() {
    return this.idToken;
  }

  getAccessToken() {
    return this.accessToken;
  }

  isAuthenticated() {
    return new Date().getTime() < this.expiresAt;
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
        // localStorage.setItem("access_token", authResult.accessToken);
        resolve(authResult);
      });
    }).then(authResult => {
      return new Promise((resolve, reject) => {
        this.auth0.client.userInfo(authResult.accessToken, function(err, user) {
          // Now you have the user's information
          if (err) return reject(err);
          resolve({ user, authResult });
        });
      }).then(data => {
        this.setSession(data);
      });
    });
  }

  setSession(data) {
    const { user, authResult } = data;
    this.profile = user;
    this.accessToken = authResult.accessToken;
    this.expiresAt = new Date().getTime() + authResult.expiresIn;
  }

  silentAuth() {
    return new Promise((resolve, reject) => {
      this.auth0.checkSession({}, (err, authResult) => {
        if (err) return reject(err);
        resolve(authResult);
      });
    }).then(authResult => {
      return new Promise((resolve, reject) => {
        this.auth0.client.userInfo(authResult.accessToken, function(err, user) {
          // Now you have the user's information
          if (err) return reject(err);
          resolve({ user, authResult });
        });
      }).then(data => {
        this.setSession(data);
      });
    });
  }

  signOut() {
    // clear id token, profile, and expiration
    this.idToken = null;
    this.profile = null;
    this.expiresAt = null;
    this.auth0.logout({
      returnTo: "http://localhost:3007",
      clientID: process.env.REACT_APP_AUTH0_CLIENT_ID
    });
  }
}

const auth = new Auth();

export default auth;