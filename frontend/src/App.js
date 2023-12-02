import deleteIcon from './delete.svg';
import downloadIcon from './download.svg'
import './App.css';
import toast, { Toaster } from 'react-hot-toast';
import React, { useState } from 'react';
import { Oval } from  'react-loader-spinner'
import { FileUploader } from "react-drag-drop-files";

const notify = (message) => toast(message);
const host = "http://ssh.jan-kupke.de:5001"

function removeFile(file_name, onDelete) {
  const data = { file_to_remove: file_name };

  fetch(`${host}/remove_file`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
  })
  .then(response => {

      return response.json();
  })
  .then(data => {
    onDelete()

  })
}    

  const download_file = (file_name) => {
    let download = document.createElement('a');
    download.href = `${host}/download_file`;
    download.download = file_name;
    download.style.display = "none";
    document.body.appendChild(download);
    download.click();  
    document.body.removeChild(download)
  }

  const init_download = (fileName) => {
    const data = { file_name: fileName };

    return fetch(`${host}/download`, {
      method: 'POST',
      headers: {
	'Content-Type': 'application/json',
      },
      mode: "no-cors",
      body: JSON.stringify(data),
    })
    .then(response => {
      return true;
    }).catch(error => {
      console.error('Fehler beim Herunterladen der Datei:', error);
      throw error; // Wiederverwenden des Fehlers für die Aufruferbehandlung
    });
  }

  function File(props) {
    const [loading, setLoading] = useState(false);

    const PrepareDownload = (file) => {
      notify("Preparing Download")
      setLoading(true);

      init_download(file).then(response => {
        if (response) {
          setLoading(false);
          download_file(file);
        }
      })
    };

    return (
      <div className='File'>
        <p>{props.name}</p>
        <div className='RightAlign'>
          <Toaster/>
          <div className='container'>
            <img src={deleteIcon} alt='delete' onClick={() => removeFile(props.name, props.onDelete)} />
          </div>
          <div className='container'>
          {loading ? (
            <Oval
              height={30}
              width={30}
              color="#F0ECE5"
              wrapperStyle={{}}
              wrapperClass=""
              visible={true}
              ariaLabel='oval-loading'
              secondaryColor="#4fa94d"
              strokeWidth={2}
              strokeWidthSecondary={2}/>
              ) : (
          <img src={downloadIcon} alt='download' onClick={() => PrepareDownload(props.name)} />
        )}
            </div>

        </div>
      </div>
    );
  }


class FileList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      files: []
    };
  }
  

  componentDidMount() {
    this.fetchFiles()
    }

  handelFileDelete = () => {
    this.fetchFiles()
  }

  updateFiles = () => {
    this.fetchFiles()
  }
  fetchFiles() {
    fetch(`${host}/files`)
      .then(response => response.json())
      .then(data => {
        this.setState({
          files: data["files"]
        });
      })
      .catch(error => console.error('Fehler beim Abrufen der Dateien:', error));
  }

  render() {

    return (
      <div>
      <div id='FileList'>
        {this.state.files.map((file) => (
          <File key={file} name={file} onDelete={this.updateFiles}/>
        ))}
      </div>
      <FileUploaderComponent render={this.updateFiles}/>
      </div>
      
    );
  }
}


class FileUploaderComponent extends React.Component {

  uploadFile = (files) => {
    let selectedFiles = Array.from(files)
    if (selectedFiles.length >= 1) {
      if (selectedFiles.length > 1) {
        notify("uploading your files...")
      } else {
        notify("uploading your file...")
      }
      selectedFiles.forEach(element => {
        const formData = new FormData();
        formData.append('file_name', element.name);
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
        notify("No files selected  ")
    }
  }


  render() {
    return (
        <div className='center'>
          <DragDrop uploadFunction={this.uploadFile}/>
        </div>)
  }
}

function DragDrop(props) {
  const [file, setFile] = useState(null);
  const handleChange = (file) => {
    props.uploadFunction(file);
    setFile(file);
  };
  return (
    <FileUploader 
      children={<p>Datei hochladen oder hier ablegen!</p>}
      classes="FileInput"
      handleChange={handleChange}
      // label="Datei hochladen oder hier ablegen!" 
      hoverTitle="" 
      multiple={true}/>
  );
}

function App() {
  return (<div>
    <FileList/>
  </div>)
}

export default App;
