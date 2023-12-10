import { host } from '../App';


export const init_download = (fileName, path) => {
  const data = { file_name: fileName, path: path };

  return fetch(`${host}/download`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    mode: "no-cors",
    body: JSON.stringify(data),
  })
    .then(response => {
      // console.log(response)
      // response = JSON.parse(response)
      // console.log(response)
      // alert("asfd")
      // return response.json()
      // download_file()
      return true;
    })
    // .then(data => {
    //   console.log(data)
    //   download_file()
    // })
    .catch(error => {
      console.error('Fehler beim Herunterladen der Datei:', error);
      throw error; // Wiederverwenden des Fehlers für die Aufruferbehandlung
    });
};
