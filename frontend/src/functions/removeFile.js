import { host } from '../App';


export function removeFile(file_name, onDelete, path, file) {
  const data = { file_to_remove: file_name, path: path.replaceAll("@@@", "/"), file: file };

  fetch(`${host}/remove_file/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'text/plain',
    },
    body: JSON.stringify(data),
  })
    .then(response => {

      return response.json();
    })
    .then(data => {
      onDelete();

    });
}
