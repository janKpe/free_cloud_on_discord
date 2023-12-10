import React from 'react';
import { DragDrop } from './DragDrop';
import { notify, host } from '../App';

export class FileUploaderComponent extends React.Component {

  uploadFile = (files) => {
    let selectedFiles = Array.from(files);
    if (selectedFiles.length >= 1) {
      if (selectedFiles.length > 1) {
        notify("uploading your files...");
      } else {
        notify("uploading your file...");
      }
      selectedFiles.forEach(element => {
        const formData = new FormData();
        formData.append('file_name', element.name);
        formData.append('path', this.props.path);
        formData.append('data', element);

        fetch(`${host}/upload`, {
          method: 'POST',
          body: formData
        })
          .then(response => response.json())
          .then(data => {
            this.props.render();
          })
          .catch(error => console.error('Fehler:', error));

      });
    } else {
      notify("No files selected  ");
    }
  };


  render() {
    return (
      <div id='StickyHeader'>
        <DragDrop uploadFunction={this.uploadFile} path={this.props.path} newRender={this.props.render} />
      </div>);
  }
}
