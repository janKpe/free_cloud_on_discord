function render_files() {
    document.getElementById("files").innerHTML = ""
    fetch('http://127.0.0.1:5000/files')
        .then(response => response.json())
        .then(data => {

            data.files.forEach((element) => {
                document.getElementById("files").innerHTML += `<li style="display: flex" ><p onclick='downloadFile("${element}")'>${element}</p> <img onclick='removeFile("${element}")' src="http://127.0.0.1:5000/delete"></li>`
            })
        })
}



    function uploadDatei() {
        const dateiInput = document.getElementById('dateiInput');
        const datei = dateiInput.files[0];
    
        if (datei) {
            const formData = new FormData();
            formData.append('file_name', datei.name);
            formData.append('data', datei);
    
            fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                render_files()
                
            })
            .catch(error => console.error('Fehler:', error));
        } else {
            console.log('Bitte eine Datei auswählen.');
        }
    }


    function downloadFile(fileName) {
        const data = { file_name: fileName };
    
        fetch('http://localhost:5000/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Erstelle einen Blob-URL und erstelle ein unsichtbares a-Element für den Download
            
            if (data.succes === true) {
                // let download = document.createElement('a');
                // download.href = "http://127.0.0.1:5000/download_file";
                // download.innerHTML = "download"
                // download.id = "huhn"
                // download.download = fileName;
                // download.style.view = "none";
                // document.body.appendChild(download);
                
                // document.getElementById("huhn").checkVisibility()
                // document.body.remove(download)
                alert("kannst")
            }
        })
        .catch(error => {
            console.error('Fehler beim Herunterladen der Datei:', error);
        });

    }
    
    function removeFile(file_name) {
        // Der Schlüssel, den du entfernen möchtest
        const data = { file_to_remove: file_name };
    
        fetch('http://localhost:5000/remove_file', {
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
            // Erstelle einen Blob-URL und erstelle ein unsichtbares a-Element für den Download

            render_files()
            
        })
      }    
    render_files()