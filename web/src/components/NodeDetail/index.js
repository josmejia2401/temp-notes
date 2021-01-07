import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import './node-detail.css';
import Composer from '../Composer';

class NoteDetail extends Component {
  constructor() {
    super()
    this.state = {
      active: false
    }
  }

  componentDidMount() {
    this.componentDidEnter();
  }

  componentWillUnmount() {
    this.componentDidAppear();
  }

  componentDidEnter() {
    this._modal.classList.add('active');
    this.setState({active: true});
  }

  componentDidAppear() {
    this._modal.classList.remove('active');
    this.setState({active: false});
  }

  _onAddItem = (item) => {

  }

  _onDeleteItem = (item) => {
    const { onDelete } = this.props;
    onDelete(item);
    this.componentDidAppear();
  }

  _onUpdateItem = (item) => {
    const { onUpdate } = this.props;
    onUpdate(item);
    this.componentDidAppear();
  }

  render() {
    const modalClass = this.state.active ? 'active' : ''
    const { note } = this.props
    return (
      <div className={`box-fill modal ${modalClass}`} ref={node => (this._modal = node)}>
        <div className="box-fill modal-backdrop" ref={node => (this._modalBackdrop = node)}/>
        <div className="modal-content center-item" ref={node => (this._modalContent = node)}>
          <Composer note={note} isEdit onSubmit={this._onUpdateItem} onDelete={this._onDeleteItem}/>
        </div>
      </div>
    );
  }
}

class NodeDetailTransition extends Component {
  render() {
    const { notes, onUpdate, onDelete } = this.props
    return (
      <Route
        path="/notes/:noteId"
        children={({ match, ...rest }) => {
          let foundNote = null;
          if (match) {
            foundNote = notes.find(note => note.id == match.params.noteId);
          }
          if (match && foundNote) {
            return (<NoteDetail onUpdate={onUpdate} onDelete={onDelete} note={foundNote}/>);
          } else {
            return null;
          }
        }}
      />
    );
  }
}

export default NodeDetailTransition;