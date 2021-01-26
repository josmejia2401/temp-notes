var BASE_URL = 'http://localhost:9000/ms/temp-notes';
if (window.location.host.includes("localhost:8080")) {
  BASE_URL = 'http://localhost:8080/ms/temp-notes';
} else if (!window.location.host.includes("localhost")) {
  BASE_URL = '/ms/temp-notes';
}

const fetchJSON = (url, option) => {
  return fetch(`${BASE_URL}${url}`, {
    ...option,
    headers: {
      'content-type': 'application/json',
    } 
  }).then(response => {
    if(response && !response.ok) {
      //return new Error('error');
      throw Error(response.statusText);
    }
    return response.json();
  });
}

export const getNotes = (username) => {
  return fetchJSON(`/${username}/get-all`);
}

export const getNote = (username, noteId) => {
  return fetchJSON(`/${username}/${noteId}/get`);
}

export const addNote = (username, note) => {
  return fetchJSON(`/${username}/create`, {
    method: 'POST',
    body: JSON.stringify(note),
  });
}

export const updateNote = (username, note) => {
  return fetchJSON(`/${username}/${note.id}/update`, {
    method: 'PUT',
    body: JSON.stringify(note),
  });
}

export const deleteNote = (username, note) => {
  return fetchJSON(`/${username}/${note.id}/delete`, {
    method: 'DELETE',
  });
}

export const login = (email, password) => {
  return fetchJSON('/auth', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
    })
  });
}

export const register = (username, password, email) => {
  return fetchJSON('/users', {
    method: 'POST',
    body: JSON.stringify({
      username,
      password,
      email,
    })
  });
}