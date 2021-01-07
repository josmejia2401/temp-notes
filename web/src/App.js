import React, { Component } from 'react';
import './App.css';
import NoteList from './components/NoteList';
import ComposerMain from './components/ComposerMain';
import NoteDetail from './components/NodeDetail';
import * as api from './api';

class App extends Component {
  constructor() {
    super();
    this.state = {
      notes: [],
      loading: true,
    };
  }

  componentDidMount() {
    this.updateData();
  }

  getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
  }

  updateData = () => {
    this.setState({
      notes: this.state.notes,
      loading: false,
    });
  };

  handleAddNote = note => {
    note.id = this.getRandomInt(0, 9999);
    this.state.notes.push(note);
    this.updateData();
  };

  handleUpdateNote = note => {
    const index = this.state.notes.findIndex(x => x.id === note.id);
    if (index !== -1) {
      this.state.notes[index] = note;
    }
    this.updateData();
    this.props.history.goBack();
  };

  handleDeleteNote = note => {
    const index = this.state.notes.findIndex(x => x.id === note.id);
    if (index !== -1) {
      this.state.notes.splice(index, 1);
    }
    this.updateData();
    this.props.history.goBack();
  };

  render() {
    const { notes, loading } = this.state;
    if (loading) {
      return (<div className="loading">loading</div>);
    } else {
      return (
        <div className="App">
          <ComposerMain onSubmit={this.handleAddNote} />
          <NoteList notes={notes} onUpdate={this.handleUpdateNote} onDelete={this.handleDeleteNote}/>
          <NoteDetail onUpdate={this.handleUpdateNote} onDelete={this.handleDeleteNote} notes={notes} location={this.props.location} />
        </div>
      );
    }
  }
}

export default App;
