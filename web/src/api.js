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
      throw Error(response.statusText);
    }
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
      return response.json();
    } else {
      return response.text();
    }
  });
}

export const getNotes = (username) => {
  return fetchJSON(`/${username}/get-all`, {
    method: 'GET'
  });
}

export const getNote = (username, noteId) => {
  return fetchJSON(`/${username}/${noteId}/get`, {
    method: 'GET'
  });
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
    method: 'DELETE'
  });
}
