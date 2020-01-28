import localStorage from "./localStorage";

function isPermittedAndOwner(permission, ownerId, resourceId) {
  if (localStorage.isPermitted(permission)) {
    if (ownerId === resourceId) {
      return true;
    }
  }

  return false;
}

export default isPermittedAndOwner;
