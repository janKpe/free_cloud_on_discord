import { host } from '../App';


export const init_download = (fileName, path) => {
  const data = { file_name: fileName, path: path };

  return fetch(`${host}/download/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    mode: "no-cors",
    body: JSON.stringify(data),
  })
    .then(response => response)
    .then(data => {
      return true 
    })
    .catch(error => {
      console.error('Fehler beim Herunterladen der Datei:', error);
      throw error; // Wiederverwenden des Fehlers für die Aufruferbehandlung
    });
};
