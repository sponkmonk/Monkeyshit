import React from 'react';
import {Button, Col, Container, Form, Row} from 'react-bootstrap';

import AuthService from '../../services/AuthService';
import monkeyGeneral from '../../images/militant-monkey.svg';
import ParticleBackground from '../ui-components/ParticleBackground';
import {Redirect} from 'react-router-dom';
import {Routes} from '../Main';

class LogoutPageComponent extends React.Component {

  redirectToLogin = () => {
    window.location.href = '/login';
  };

  constructor(props) {
    super(props);
    fetch('/api/logout').then(this.redirectToLogin);
  }

  render() {
    return (<p>Logging out</p>);
  }
}

export default LogoutPageComponent;
