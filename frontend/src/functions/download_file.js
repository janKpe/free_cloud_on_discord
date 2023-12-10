import { host } from '../App';


export const download_file = (file_name) => {
  let download = document.createElement('a');
  download.href = `${host}/download_file`;
  download.download = file_name;
  download.style.display = "none";
  document.body.appendChild(download);
  download.click();
  document.body.removeChild(download);
};
