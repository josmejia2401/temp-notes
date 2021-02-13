import React, { PureComponent } from 'react';
import './note.css';

class Note extends PureComponent {
  render() {
    const { title, description, updateAt, onClick } = this.props;
    var today = new Date(updateAt).toISOString().slice(0, 10);
    var dRemaining = new Date(updateAt);
    var Dias_Restantes  = (5 - (Math.abs(new Date() - dRemaining) / (1000 * 3600 * 24))).toFixed(2);
    return (
      <div>
        <div className="card note" onClick={onClick}>
          {title && <div className="note-title">{title}</div>}
          <div className="note-content" dangerouslySetInnerHTML={{__html: description}}/>
          {updateAt && <div className="note-updateAt">{today} ({Dias_Restantes} días)</div>}
        </div>
      </div>
    );
  }
}

export default Note;
