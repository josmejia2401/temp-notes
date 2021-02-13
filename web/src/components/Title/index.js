import React, { Component } from 'react';
import './composer.css';

class Title extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { isEdit } = this.props;
    return (
      <div className={`composer-container`}>
        <p>Las notas se eliminaran de manera autómatica después de 5 días de no actualización.</p>
      </div>
    );
  }
}

export default Title;
