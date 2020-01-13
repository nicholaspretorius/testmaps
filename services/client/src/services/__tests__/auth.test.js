import auth from "./../auth";

it("handleAuthentication should return a promise", () => {
  auth
    .handleAuthentication()
    .then(res => {
      expect(res).toBeTruthy();
    })
    .catch(err => {
      expect(err).toBeFalsy();
    });
});

it("silentAuth should return a promise", () => {
  auth
    .silentAuth()
    .then(res => {
      expect(res).toBeFalsy();
    })
    .catch(err => {
      expect(err).toBeTruthy();
    });
});
