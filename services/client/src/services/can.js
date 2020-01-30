import localStorage from "./localStorage";

function isPermittedAndOwner(permission, ownerId, resourceId) {
  const superadmins = [
    "auth0|5e329997b5be300ef6889c4c",
    "google-oauth2|104755831296456998532"
  ];

  if (localStorage.isPermitted(permission)) {
    if (ownerId === resourceId || superadmins.includes(ownerId)) {
      return true;
    }
  }

  return false;
}

export default isPermittedAndOwner;
