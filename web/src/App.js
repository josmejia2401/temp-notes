import React, { Component } from 'react';
import NoteList from './components/NoteList';
import InputNote from './components/InputNote';
import NoteDetail from './components/NodeDetail';
import Access from './components/Access'
import Title from './components/Title'
import * as api from './api';

import './App.css';
import logo from './logo.svg';

function PreLoading() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>car<code>GAN</code>go</p>
        <a className="App-link">Haciendo cosas increíbles</a>
      </header>
    </div>
  );
}

class App extends Component {
  constructor() {
    super();
    this.state = {
      notes: [],
      loading: true,
      isAccessUsername: false
    };
  }

  componentDidMount() {
    this.getData();
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

  getData = () => {
    api.getNotes('josmejia2401').then(result => {
      if (result) {
        this.state.notes = result;
      }
      this.updateData();
    }).catch(error => {
      console.log(error);
      this.updateData();
    });
  }

  handleAddNote = note => {
    //note.id = this.getRandomInt(0, 9999);
    //this.state.notes.push(note);
    //this.updateData();
    this.setState({ loading: true });
    api.addNote('josmejia2401', note).then(result => {
      if (result) {
        this.state.notes.push(result);
        this.updateData();
      }
    }).catch(error => {
      console.log(error);
      this.updateData();
    });
  };

  handleUpdateNote = note => {
    this.setState({ loading: true });
    api.updateNote('josmejia2401', note).then(result => {
      if (result) {
        const index = this.state.notes.findIndex(x => x.id === note.id);
        if (index !== -1) {
          this.state.notes[index] = note;
          this.updateData();
        }
        this.props.history.goBack();
      }
    }).catch(error => {
      console.log(error);
      this.updateData();
    });
  };

  handleDeleteNote = note => {
    this.setState({ loading: true });
    api.deleteNote('josmejia2401', note).then(result => {
      if (result) {
        const index = this.state.notes.findIndex(x => x.id === note.id);
        if (index !== -1) {
          this.state.notes.splice(index, 1);
          this.updateData();
        }
        this.props.history.goBack();
      }
    }).catch(error => {
      console.log(error);
      this.updateData();
    });
  };

  handleIsAccessUsername = (isAccessUsername) => {
    this.setState({isAccessUsername: isAccessUsername});
  }

  renderNotes = () => {
    const { notes } = this.state;
    return (
      <div>
        <Title/>
        <InputNote onSubmit={this.handleAddNote} history={this.props.history} />
        <NoteList notes={notes} onUpdate={this.handleUpdateNote} onDelete={this.handleDeleteNote} history={this.props.history} />
        <NoteDetail onUpdate={this.handleUpdateNote} onDelete={this.handleDeleteNote} notes={notes} location={this.props.location} history={this.props.history} />
      </div>
    );
  }

  render() {
    const { notes, loading } = this.state;
    if (loading) {
      return  PreLoading();
    } else {
      return (
        <div className="App">
          { !this.state.isAccessUsername && <Access handleIsAccessUsername={this.handleIsAccessUsername} location={this.props.location} history={this.props.history}></Access>}
          { this.state.isAccessUsername && <this.renderNotes/> }
        </div>
      );
    }
  }
}

export default App;
