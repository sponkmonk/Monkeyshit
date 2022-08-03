import decode from 'jwt-decode';

export default class AuthService {
  SECONDS_BEFORE_JWT_EXPIRES = 20;
  AUTHENTICATION_API_ENDPOINT = '/api/auth';
  REGISTRATION_API_ENDPOINT = '/api/registration';

  login = (username, password) => {
    return this._login(username, password);
  };

  authFetch = (url, options) => {
    return this._authFetch(url, options);
  };

  jwtHeader = () => {
    if (this.loggedIn()) {
      return 'Bearer ' + this._getToken();
    }
  };

  _login = (username, password) => {
    return this._authFetch(this.AUTHENTICATION_API_ENDPOINT, {
      method: 'POST',
      body: JSON.stringify({
        username,
        password
      })
    }).then(response => response.json())
      .then(res => {
        return res["login"]
      })
  };

  register = (username, password) => {
    return this._register(username, password);
  };

  _register = (username, password) => {
    return this._authFetch(this.REGISTRATION_API_ENDPOINT, {
      method: 'POST',
      body: JSON.stringify({
        'username': username,
        'password': password
      })
    }).then(res => {
      if (res.status === 200) {
        return this._login(username, password)
      } else {
        return res.json().then(res_json => {
          return {result: false, error: res_json['error']};
        })
      }
    })
  };

  _authFetch = (url, options = {}) => {
    return fetch(url, options)
      .then(res => {
        return res;
      })
  };

  needsRegistration = () => {
    return fetch(this.REGISTRATION_API_ENDPOINT,
      {method: 'GET'})
      .then(response => response.json())
      .then(res => {
        return res['needs_registration']
      })
  };

  loggedIn() {
     return fetch(this.AUTHENTICATION_API_ENDPOINT)
      .then(response => response.json())
      .then(res => {
        console.log(res);
        return res['authenticated'];
      })
  }

  logout = () => {
    this._removeToken();
  };

  _isTokenExpired(token) {
    try {
      return decode(token)['exp'] - this.SECONDS_BEFORE_JWT_EXPIRES < Date.now() / 1000;
    } catch (err) {
      return false;
    }
  }

  _setToken(idToken) {
    localStorage.setItem('jwt', idToken);
  }

  _removeToken() {
    localStorage.removeItem('jwt');
  }

  _getToken() {
    return localStorage.getItem('jwt')
  }

}
