function getItem(item) {
  return window.localStorage.getItem(item);
}

function setItem(item, value) {
  return window.localStorage.setItem(item, value);
}

function removeItem(item) {
  return window.localStorage.removeItem(item);
}

const localStorage = {
  getItem,
  setItem,
  removeItem
};

export default localStorage;
