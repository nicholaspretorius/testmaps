function getItem(item) {
  return window.localStorage.getItem(item);
}

function setItem(item, value) {
  return window.localStorage.setItem(item, value);
}

function removeItem(item) {
  return window.localStorage.removeItem(item);
}

function getPermissions() {
  return localStorage.getItem("permissions");
}

function isPermitted(permission) {
  const permissions = getPermissions();

  if (permissions) {
    return permissions.includes(permission);
  }
}

const localStorage = {
  getItem,
  setItem,
  removeItem,
  getPermissions,
  isPermitted
};

export default localStorage;
