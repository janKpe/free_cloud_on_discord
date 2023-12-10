import React, { useState } from 'react';
import { FileUploader } from "react-drag-drop-files";
import { host } from '../App';

export function DragDrop(props) {
  const [file, setFile] = useState(null);

  const containsInvalidCharacters = (filename) => {
    return filename && (filename.includes('/') || filename.includes('@@@'));
  };
  
  const handleChange = (files) => {
    let selectedFiles = Array.from(files);

    const hasInvalidFile = selectedFiles.some(file => containsInvalidCharacters(file.name));

    if (hasInvalidFile) {
      alert("One or more file names contain invalid characters. They cannot contain '/' or '@@@'.");
      return;
    }

    props.uploadFunction(files);
    setFile(files);
  };
  const newFolder = () => {
    let folder_name = prompt("Folder Name:")

    if (folder_name && (folder_name.includes('/') || folder_name.includes('@@@'))) {
      alert("Invalid folder name. The folder name cannot contain '/' or '@@@'.");
      return;
    }
  
    let data = { path: props.path, folder_name: folder_name };
    fetch(`${host}/newFolder`, {
      method: 'POST',
      mode: "no-cors",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then(response => {

        props.newRender();
      });

  };
  return (
    <div className='center' id='FileUploadParrent'>
      <FileUploader
        children={<p>Upload file or drop it here!</p>}
        classes="FileInput"
        handleChange={handleChange}
        hoverTitle=""
        multiple={true} />
      <button className='FileInput' onClick={() => newFolder()}>new folder</button>

    </div>
  );
}
