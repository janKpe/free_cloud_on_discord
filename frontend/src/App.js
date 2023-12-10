import arrowBack from './assets/arrow_back.svg'
import './style/App.css';
import toast from 'react-hot-toast';
import React from 'react';
import { useParams } from "react-router-dom";
import { File } from './components/File';
import { Tile } from './components/Tile';
import { FileUploaderComponent } from './components/FileUploaderComponent';


export const notify = (message) => toast(message);
export const host = "http://ssh.jan-kupke.de:5001"

class FileList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      files: [],
      folders: []
    };
  }
  
  componentDidMount() {

    if (this.props.useParams === true) {
      this.fetchFiles(this.props.path["path"].replaceAll("@@@", "/"))
    } else {
      window.location.href = "@@@"
      this.fetchFiles()      
    }
  }

  handelFileDelete = () => {
    if (this.props.useParams === true) {
      
      this.fetchFiles(this.props.path["path"].replaceAll("@@@", "/"))
    } else {
      this.fetchFiles()      
    }
  }

  updateFiles = () => {
    if (this.props.useParams === true) {
      
      this.fetchFiles(this.props.path["path"].replaceAll("@@@", "/"))
    } else {
      this.fetchFiles()      
    }
  }
  
  fetchFiles(path="/") {
    if (path != "/") {
      path = "/" + path
    }
    let data = { path: path} 
    fetch(`${host}/files`, {
      method: 'POST',
      body: JSON.stringify(data)
    }
      )
      .then(response => response.json())
      .then(data => {
        this.setState({
          files: data["files"],
          folders: data["dirs"]
        });
      })
      .catch(error => console.error('Fehler beim Abrufen der Dateien:', error));
  }

  pageBackCallback() {
    if (this.props.useParams === true) {
      let newPath = this.props.path["path"];
      newPath = newPath.split("@@@");
      newPath.pop()
      newPath.pop()
      window.location.href = newPath.join("@@@") + "@@@"; 
    }
  }

  newFolder() {

  }
  render() {

    return (
      <div>
        <FileUploaderComponent render={this.updateFiles} path={this.props.path["path"]}/>
        <div id='navigator'>
          <Tile child={
            <div className='center'> 
              <p>{this.props.useParams ? (this.props.path["path"].replaceAll("@@@", "/")) : "/"}</p>
            </div>
          } />
          <Tile child={
            <div className='center' onClick={() => {this.pageBackCallback()} }>
              <img src={arrowBack} alt='back'/>
            </div>} />
        </div>
        <div id='FileList'>
          {this.state.folders.map((folder) => (
              <File key={folder} name={folder} onDelete={this.updateFiles} file={ false } path={this.props.path["path"]}/>
            ))}

          {this.state.files.map((file) => (
            <File key={file} name={file} onDelete={this.updateFiles} file={ true } path={this.props.path["path"]}/>
          ))}
        </div>
      </div>
      
    );
  }
}


function App(props) {

  let path = useParams();
  return (
    <FileList useParams={props.useParams} path={path}/>
  ) 

}

export default App;
