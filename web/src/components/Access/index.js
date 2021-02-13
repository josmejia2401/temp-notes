import React, { Component } from 'react';
import './composer.css';
import Input from '../Input';
import Button from '../Button';

class Access extends Component {

  constructor(props) {
    super(props);
    this.state = {
      isAccessUsername : false,
      access: {
        username: {
          value: ''
        },
        password: {
          value: ''
        }
      }
    };;
  };

  componentDidMount() {
    this.getAccessUsername();
  };


  handleChange = event => {
    if (event && event.target) {
      const fieldName = event.target.name;
      let access = this.state.access;
      access[fieldName] = { value: event.target.value };
      this.setState({ access: access });
    }
  };

  handleSubmit = e => {
    e.preventDefault();
    //onSubmit(this.state.access);
    //consumir el servicio que da el acceso
    this.props.handleIsAccessUsername(true);
  };


  handleCancel = e => {
    if (e && e.target) {
      e.preventDefault();
      //this.props.history.goBack();
    }
  };

  getAccessUsername = (e) => {
    const accessUsername = window.localStorage.getItem('accessUsername');
    if (accessUsername) {
      this.setState({ isAccessUsername: true });
    } else {
      this.setState({ isAccessUsername: false });
    }
    this.props.handleIsAccessUsername(this.state.isAccessUsername);
  }

  getValue = fieldName => {
    let val = this.state.access[fieldName].value;
    return val;
  };

  render() {
    const modalClass = this.state.isAccessUsername ? '' : 'active';
    return (
      <div className={`box-fill modal ${modalClass}`} ref={node => (this._modal = node)}>
        <div className="box-fill modal-backdrop" ref={node => (this._modalBackdrop = node)}/>
        <div className="modal-content center-item" ref={node => (this._modalContent = node)}>
          <div className={`card composer-container edit`}>
            <form onSubmit={this.handleSubmit} className="input-form">
              <Input
                type="text"
                name="username"
                placeholder="Username"
                autoComplete={"false"}
                autoFocus
                value={this.getValue('username')}
                onChange={this.handleChange}
                style={{ 'marginBottom': '5px' }}
              />
              <Input
                type="text"
                name="password"
                placeholder="Palabra clave"
                autoComplete={"false"}
                autoFocus
                value={this.getValue('password')}
                onChange={this.handleChange}
                style={{  'marginTop': '5px' }}
              />
              <div className="actions">
                <Button>Iniciar</Button>
                <Button onClick={this.handleCancel}>Cancelar</Button>
              </div>
            </form>
          </div>
          </div>
      </div>
    );
  };
}

export default Access;
