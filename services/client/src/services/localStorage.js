class LocalStorage {
  constructor() {
    this.getItem = this.getItem.bind(this);
    this.setItem = this.setItem.bind(this);
    this.removeItem = this.removeItem.bind(this);
  }

  getItem(item) {
    return window.localStorage.getItem(item);
  }

  setItem(item, value) {
    return window.localStorage.setItem(item, value);
  }

  removeItem(item) {
    return window.localStorage.removeItem(item);
  }
}

const localStorage = new LocalStorage();

export default localStorage;
