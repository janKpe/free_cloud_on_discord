import deleteIcon from '../assets/delete.svg';
import downloadIcon from '../assets/download.svg';
import file from '../assets/file.svg';
import folder from '../assets/folder.svg';
import { Toaster } from 'react-hot-toast';
import React, { useState } from 'react';
import { Oval } from 'react-loader-spinner';
import { notify } from '../App';
import { removeFile } from '../functions/removeFile';
import { download_file } from '../functions/download_file';
import { init_download } from '../functions/init_download';

export function File(props) {
  const [loading, setLoading] = useState(false);

  const PrepareDownload = (file, path) => {
    notify("Preparing Download");
    setLoading(true);

    init_download(file, path).then(response => {
      if (response) {
        setLoading(false);
        download_file(file);
      }
    });
  };

  const redirect = () => {
    if (props.file === false) {
      window.location.href = window.location.href + `${props.name}` + "@@@";
    }
  };
  return (
    <div className='File' onClick={() => redirect()} id='test'>
      <div className='LeftAlign'>
        {props.file ? (<img src={file} alt='file' />) : (
          <img src={folder} alt='folder' />
        )}
      </div>
      <p>{props.name}</p>
      <div className='RightAlign'>
        <Toaster />
        <div className='container'>
          <img id="die_sonne" src={deleteIcon} alt='delete' onClick={(e) => {
            e.stopPropagation();
            removeFile(props.name, props.onDelete, props.path, props.file);
          }} />
        </div>
        {props.file && (
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
                strokeWidthSecondary={2} />
            ) : (
              <img src={downloadIcon} alt='download' onClick={() => PrepareDownload(props.name, props.path.replaceAll("@@@", "/"))} />
            )}
          </div>
        )}
      </div>
    </div>
  );
  
}
