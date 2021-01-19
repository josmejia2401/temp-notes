import React, { Component } from 'react';
import './composer.css';
import Input from '../Input';
import Button from '../Button';
import Textarea from '../Textarea';

const initialState = {
  title: {
    value: ''
  },
  description: {
    value: ''
  }
};

const noteToState = note => {
  return {
    title: {
      value: note.title,
    },
    description: {
      value: note.description,
    }
  };
}

class Composer extends Component {

  constructor(props) {
    super(props);
    this.handleResize = this.handleResize.bind(this);
    this.textAreaRef = React.createRef();//React.useRef();//React.createRef();
    let state = initialState;
    if (props.note) {
      state = noteToState(props.note);
    } else if (window.activeNote && window.activeNote.note) {
      state = noteToState(window.activeNote.note);
    }
    window.activeNote = {};
    this.state = state;
  };

  componentDidMount() {
    this.onResize();
  };

  onResize = () => {
    if (this.textAreaRef && this.textAreaRef.current) {
      const textAreaComposerEdit = document.getElementById("textAreaComposerEdit");
      if (textAreaComposerEdit) {
        textAreaComposerEdit.style.height = 'auto';
        textAreaComposerEdit.style.height = textAreaComposerEdit.scrollHeight + 'px';
      }
    }
  };


  handleChange = event => {
    const fieldName = event.target.name;
    this.setState({
      [fieldName]: {
        value: event.target.value
      }
    });
  };

  handleSubmit = e => {
    e.preventDefault();
    const { onSubmit, note } = this.props;
    // TODO: validate
    const title = this.state.title.value;
    // convert line break to </br> tag
    let description = "";
    description = this.state.description.value.replace(/\n/g, '</br>');
    const newNote = {
      title,
      description
    }
    if (note) {
      newNote.id = note.id;
    }
    onSubmit(newNote);
    this.setState(initialState);
  };

  handleDelete = event => {
    event.preventDefault();
    this.props.onDelete && this.props.onDelete(this.props.note);
  };

  handleResize = e => {
    if (e && e.target) {
      const element = e.target;
      element.style.height = 'auto';
      element.style.height = element.scrollHeight + 'px';
    }
  };

  handleCancel = e => {
    if (e && e.target) {
      e.preventDefault();
      this.props.history.goBack();
    }
  };

  getValue = fieldName => {
    let val = this.state[fieldName].value;
    val = val.replace(/<\s*\/?br\s*[\/]?>/g, '\n');
    return val;
  };

  render() {
    const { isEdit } = this.props;
    return (
      <div className={`card composer-container ${isEdit ? 'edit' : ''}`}>
        <form onSubmit={this.handleSubmit} className="input-form">
          <Input
            type="text"
            name="title"
            placeholder="Title"
            autoComplete={"false"}
            autoFocus
            value={this.getValue('title')}
            onChange={this.handleChange}
            style={{ 'marginBottom': '5px' }}
          />
          <Textarea
            id="textAreaComposerEdit"
            autoFocus
            ref={this.textAreaRef}
            className="note-description"
            name="description"
            placeholder="Take a note..."
            value={this.getValue('description')}
            onChange={this.handleChange}
            onInput={this.handleResize}
            style={{ 'marginTop': '5px' }}
          />
          <div className="actions">
            <Button>Actualizar</Button>
            {isEdit && <Button onClick={this.handleDelete}>Delete</Button>}
            <Button onClick={this.handleCancel}>Cancel</Button>
          </div>
        </form>
      </div>
    );
  };
}

export default Composer;
